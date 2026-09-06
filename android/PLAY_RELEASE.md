# Publicacion Android

Paquete confirmado: `com.bfjgames.llc`.

Actualizacion: la app usa Google Play Billing directo (ver `SubscriptionBridge.kt`), sin RevenueCat por ahora. Se podria reconectar RevenueCat mas adelante para compartir el entitlement con la version web; mientras tanto Android no depende de el.

## Configuracion local

Copiar `release.properties.example` a `release.properties`. Completar los datos de una clave de subida propia (no hace falta ninguna clave de API mientras se use Billing directo). No compartir contrasenas ni subir el archivo de firma al repositorio. Conservar una copia segura de la clave.

La firma local es opcional: tambien se puede usar Android Studio > Build > Generate Signed Bundle / APK > Android App Bundle. Sin firma local ni firma proporcionada por Android Studio, el bundle generado no estara firmado y no se debe subir a Play.

Para compilar desde consola:

```powershell
cd android
.\gradlew.bat bundleRelease
```

Resultado esperado: `app/build/outputs/bundle/release/app-release.aab`.

## Google Play Billing (directo, sin RevenueCat)

1. Crear o seleccionar la app en Play Console y configurar el perfil de pagos.
2. Configurar Play App Signing y subir el AAB firmado a pruebas internas.
3. Crear la suscripcion con ID `suscripcion_id_001` y el plan base `vipsuscription001`. Configurar un precio base de **S/ 7.90 PEN al mes**; en Play Console usa la opcion de precios locales para que Google aplique el tipo de cambio y el redondeo correspondiente a cada pais o region. Define los paises disponibles, el periodo mensual y activa el plan. El ID del producto no se puede cambiar despues de crearlo.
4. Incrementar versionCode y volver a generar el AAB con `SubscriptionBridge.kt` (usa `com.android.billingclient:billing` directamente contra ese ID de producto, sin claves externas que configurar).
5. Configurar probadores de licencia e instalar desde el enlace de pruebas de Google Play. Verificar compra, cancelacion, compra pendiente, renovacion, vencimiento y recuperacion del acceso tras reinstalar e iniciar sesion.

## Pendientes antes de produccion

- No hay backend que valide los recibos de compra ni las Real-time Developer Notifications de Google — `checkStatus()` solo reporta si Play considera la suscripcion comprada en este momento, sin fecha real de vencimiento ni deteccion de reembolsos/chargebacks. Revisar antes de depender de esto en produccion.
- El otorgamiento mensual de monedas ocurre en JavaScript/localStorage usando el mes calendario del dispositivo (no la fecha real de renovacion, que no esta disponible sin backend); revisar su persistencia y validacion en servidor antes de vender ese beneficio.
- Verificar el backend HTTPS del juego desde un dispositivo real.
- Confirmar precio y condiciones visibles de la suscripcion y el flujo de restauracion.
- Completar ficha, capturas, icono, politica de privacidad, seguridad de datos, clasificacion, anuncios y acceso para revision. Revisar eliminacion de cuenta porque el juego ofrece registro.
- Cumplir las pruebas cerradas que Play Console exija para la cuenta.
- No se ha generado ni subido un AAB de publicacion todavia.
- Si en el futuro se reconecta RevenueCat (para compartir el entitlement con la version web), ver las referencias de abajo.

Referencias:
- https://developer.android.com/google/play/billing/integrate
- https://developer.android.com/google/play/billing/test
- https://support.google.com/googleplay/android-developer/answer/14151465
- https://www.revenuecat.com/docs/getting-started/entitlements/android-products
- https://www.revenuecat.com/docs/service-credentials/creating-play-service-credentials
