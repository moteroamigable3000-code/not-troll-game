package com.bfjstudios.nottroll.android

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.webkit.JavascriptInterface
import android.webkit.WebView
import com.bfjstudios.nottroll.BuildConfig
import com.revenuecat.purchases.CustomerInfo
import com.revenuecat.purchases.Package
import com.revenuecat.purchases.PurchaseParams
import com.revenuecat.purchases.Purchases
import com.revenuecat.purchases.getCustomerInfoWith
import com.revenuecat.purchases.getOfferingsWith
import com.revenuecat.purchases.logInWith
import com.revenuecat.purchases.purchaseWith
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone

// Bridges game.js's Subscription module (see game.js) to the RevenueCat
// Android SDK, which wraps Google Play Billing — required by Play Store
// policy for digital goods bought inside the app. Exposed to the WebView as
// window.AndroidBilling (wired up in MainActivity.onCreate). Every result
// posts back into the page via the same window.onAndroidSubscription*
// callbacks the web build's RevenueCat SDK feeds directly.
private const val ENTITLEMENT_ID = "premium"

class SubscriptionBridge(private val activity: Activity, private val webView: WebView) {

    @JavascriptInterface
    fun identify(playerId: String) {
        if (!billingReady()) return
        Purchases.sharedInstance.logInWith(playerId, onError = { pushError(it.message) }) { _, _ ->
            checkStatus()
        }
    }

    @JavascriptInterface
    fun checkStatus() {
        if (!billingReady()) return
        Purchases.sharedInstance.getCustomerInfoWith(onError = { pushError(it.message) }) { info ->
            pushStatus(info)
        }
    }

    @JavascriptInterface
    fun purchase() {
        if (!billingReady()) return
        activity.runOnUiThread {
        Purchases.sharedInstance.getOfferingsWith(onError = { pushError(it.message) }) { offerings ->
            val pkg: Package? = offerings.current?.availablePackages?.firstOrNull()
            if (pkg == null) {
                pushError("No hay oferta de suscripcion configurada.")
                return@getOfferingsWith
            }
            Purchases.sharedInstance.purchaseWith(
                PurchaseParams.Builder(activity, pkg).build(),
                onError = { error, userCancelled -> if (!userCancelled) pushError(error.message) },
                onSuccess = { _, info -> pushStatus(info) }
            )
        }
        }
    }

    private fun billingReady(): Boolean {
        if (BuildConfig.REVENUECAT_API_KEY.startsWith("goog_")) return true
        pushError("Las compras todavia no estan configuradas.")
        return false
    }

    @JavascriptInterface
    fun manage() {
        activity.startActivity(
            Intent(Intent.ACTION_VIEW, Uri.parse("https://play.google.com/store/account/subscriptions"))
        )
    }

    private fun pushStatus(info: CustomerInfo) {
        val entitlement = info.entitlements[ENTITLEMENT_ID]
        val active = entitlement?.isActive == true
        val expiresAt = entitlement?.expirationDate?.let { isoFormat(it) }
        val js = "window.onAndroidSubscriptionStatus && window.onAndroidSubscriptionStatus(" +
            active + ", " + (if (expiresAt != null) JSONObject.quote(expiresAt) else "null") + ")"
        webView.post { webView.evaluateJavascript(js, null) }
    }

    private fun pushError(message: String?) {
        val js = "window.onAndroidSubscriptionError && window.onAndroidSubscriptionError(" +
            JSONObject.quote(message ?: "Error desconocido") + ")"
        webView.post { webView.evaluateJavascript(js, null) }
    }

    private fun isoFormat(date: Date): String {
        val formatter = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", Locale.US)
        formatter.timeZone = TimeZone.getTimeZone("UTC")
        return formatter.format(date)
    }
}
