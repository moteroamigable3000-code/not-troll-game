package com.bfjstudios.nottroll.android

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.webkit.JavascriptInterface
import android.webkit.WebView
import com.android.billingclient.api.AcknowledgePurchaseParams
import com.android.billingclient.api.BillingClient
import com.android.billingclient.api.BillingClient.BillingResponseCode
import com.android.billingclient.api.BillingClientStateListener
import com.android.billingclient.api.BillingFlowParams
import com.android.billingclient.api.BillingResult
import com.android.billingclient.api.PendingPurchasesParams
import com.android.billingclient.api.Purchase
import com.android.billingclient.api.PurchasesUpdatedListener
import com.android.billingclient.api.QueryProductDetailsParams
import com.android.billingclient.api.QueryPurchasesParams
import org.json.JSONObject

// Bridges game.js's Subscription module (see game.js) directly to the Google
// Play Billing Library — no RevenueCat middle layer for now (a cross-platform
// entitlement backend via RevenueCat may be reconnected later; see
// PLAY_RELEASE.md). Exposed to the WebView as window.AndroidBilling (wired up
// in MainActivity.onCreate). Every result posts back into the page via the
// same window.onAndroidSubscription* callbacks a future backend would use.
//
// There's no server here to verify receipts or track renewals, so
// checkStatus() only reports whether Play currently considers the
// subscription purchased — it can't report a real expiration date (that
// requires the Play Developer API). game.js derives its monthly-coins period
// from the current calendar month instead of that date for this reason.
private const val SUBSCRIPTION_PRODUCT_ID = "suscripcion_id_001"

class SubscriptionBridge(private val activity: Activity, private val webView: WebView) {

    private val purchasesUpdatedListener = PurchasesUpdatedListener { result, purchases ->
        when (result.responseCode) {
            BillingResponseCode.OK -> purchases?.forEach { handlePurchase(it) }
            BillingResponseCode.USER_CANCELED -> { /* no-op, matches prior behavior */ }
            else -> pushError(result.debugMessage)
        }
    }

    // Subscriptions get pending-purchase support automatically — no
    // PendingPurchasesParams opt-in needed unless we sell one-time products.
    private val billingClient: BillingClient = BillingClient.newBuilder(activity)
        .setListener(purchasesUpdatedListener)
        .enablePendingPurchases(PendingPurchasesParams.newBuilder().build())
        .enableAutoServiceReconnection()
        .build()

    init {
        billingClient.startConnection(object : BillingClientStateListener {
            override fun onBillingSetupFinished(billingResult: BillingResult) {
                if (billingResult.responseCode == BillingResponseCode.OK) checkStatus()
                else pushError(billingResult.debugMessage)
            }
            override fun onBillingServiceDisconnected() { /* enableAutoServiceReconnection retries */ }
        })
    }

    @JavascriptInterface
    fun identify(playerId: String) {
        // No backend yet to key entitlements by our own player_id — Play
        // Billing ties a purchase to the signed-in Play Store account.
    }

    @JavascriptInterface
    fun checkStatus() {
        if (!billingClient.isReady) return
        val params = QueryPurchasesParams.newBuilder()
            .setProductType(BillingClient.ProductType.SUBS)
            .build()
        billingClient.queryPurchasesAsync(params) { result, purchases ->
            if (result.responseCode != BillingResponseCode.OK) {
                pushError(result.debugMessage)
                return@queryPurchasesAsync
            }
            val active = purchases.firstOrNull {
                it.products.contains(SUBSCRIPTION_PRODUCT_ID) && it.purchaseState == Purchase.PurchaseState.PURCHASED
            }
            pushStatus(active != null)
            if (active != null && !active.isAcknowledged) acknowledge(active)
        }
    }

    @JavascriptInterface
    fun purchase() {
        if (!billingClient.isReady) {
            pushError("La tienda de Google Play no esta disponible todavia.")
            return
        }
        val params = QueryProductDetailsParams.newBuilder()
            .setProductList(listOf(
                QueryProductDetailsParams.Product.newBuilder()
                    .setProductId(SUBSCRIPTION_PRODUCT_ID)
                    .setProductType(BillingClient.ProductType.SUBS)
                    .build()
            ))
            .build()
        billingClient.queryProductDetailsAsync(params) { result, productDetailsResult ->
            if (result.responseCode != BillingResponseCode.OK) {
                pushError(result.debugMessage)
                return@queryProductDetailsAsync
            }
            val details = productDetailsResult.productDetailsList.firstOrNull()
            val offer = details?.subscriptionOfferDetails?.firstOrNull()
            if (details == null || offer == null) {
                pushError("La suscripcion $SUBSCRIPTION_PRODUCT_ID no tiene una oferta activa en Play Console.")
                return@queryProductDetailsAsync
            }
            val flowParams = BillingFlowParams.newBuilder()
                .setProductDetailsParamsList(listOf(
                    BillingFlowParams.ProductDetailsParams.newBuilder()
                        .setProductDetails(details)
                        .setOfferToken(offer.offerToken)
                        .build()
                ))
                .build()
            activity.runOnUiThread {
                val launchResult = billingClient.launchBillingFlow(activity, flowParams)
                if (launchResult.responseCode != BillingResponseCode.OK) pushError(launchResult.debugMessage)
            }
        }
    }

    fun endConnection() {
        billingClient.endConnection()
    }

    @JavascriptInterface
    fun manage() {
        activity.startActivity(
            Intent(Intent.ACTION_VIEW, Uri.parse("https://play.google.com/store/account/subscriptions"))
        )
    }

    private fun handlePurchase(purchase: Purchase) {
        if (!purchase.products.contains(SUBSCRIPTION_PRODUCT_ID)) return
        when (purchase.purchaseState) {
            Purchase.PurchaseState.PURCHASED -> {
                pushStatus(true)
                if (!purchase.isAcknowledged) acknowledge(purchase)
            }
            Purchase.PurchaseState.PENDING ->
                pushError("Compra pendiente: se confirmara cuando se complete el pago.")
            else -> { /* unspecified state, nothing to report */ }
        }
    }

    private fun acknowledge(purchase: Purchase) {
        val params = AcknowledgePurchaseParams.newBuilder()
            .setPurchaseToken(purchase.purchaseToken)
            .build()
        billingClient.acknowledgePurchase(params) { result ->
            if (result.responseCode != BillingResponseCode.OK) pushError(result.debugMessage)
        }
    }

    private fun pushStatus(active: Boolean) {
        val js = "window.onAndroidSubscriptionStatus && window.onAndroidSubscriptionStatus(" +
            active + ", null)"
        webView.post { webView.evaluateJavascript(js, null) }
    }

    private fun pushError(message: String?) {
        val js = "window.onAndroidSubscriptionError && window.onAndroidSubscriptionError(" +
            JSONObject.quote(message ?: "Error desconocido") + ")"
        webView.post { webView.evaluateJavascript(js, null) }
    }
}
