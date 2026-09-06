# Publicacion Android

Paquete confirmado: `com.bfjgames.llc`.

Actualizacion: se usara Google Play Billing directo. La migracion del codigo de compras esta pendiente; las instrucciones de RevenueCat de abajo son historicas y no son requisitos para compilar.

## Configuracion local

Copiar `release.properties.example` a `release.properties`. Completar la clave publica Android de RevenueCat y los datos de una clave de subida propia. No compartir contrasenas ni subir el archivo de firma al repositorio. Conservar una copia segura de la clave.

La firma local es opcional: tambien se puede usar Android Studio > Build > Generate Signed Bundle / APK > Android App Bundle. Sin firma local ni firma proporcionada por Android Studio, el bundle generado no estara firmado y no se debe subir a Play.

Para compilar desde consola:

```powershell
cd android
.\gradlew.bat bundleRelease
```

Resultado esperado: `app/build/outputs/bundle/release/app-release.aab`.

## Google Play y RevenueCat

1. Crear o seleccionar la app en Play Console y configurar el perfil de pagos.
2. Configurar Play App Signing y subir el AAB firmado a pruebas internas.
3. Crear la suscripcion y su plan base, definir precio, moneda, paises y periodo; activar el plan. Estos datos todavia estan pendientes de definir.
4. Crear la app Google Play en RevenueCat con el mismo paquete. Conectar las credenciales de servicio siguiendo su guia oficial; guardarlas en RevenueCat, nunca en el juego.
5. Importar el producto de Play en RevenueCat, asociarlo al entitlement exacto `premium` y agregarlo a la offering actual. El codigo existente compra el primer paquete de esa offering: mantener una unica opcion hasta implementar un selector.
6. Copiar la clave publica Android `goog_...` a la configuracion local y volver a generar el AAB. Incrementar versionCode para cada nueva subida.
7. Configurar probadores de licencia e instalar desde el enlace de pruebas de Google Play. Verificar compra, cancelacion, compra pendiente, renovacion, vencimiento y recuperacion del acceso tras reinstalar e iniciar sesion.

## Pendientes antes de produccion

- Verificar el backend HTTPS del juego desde un dispositivo real.
- Confirmar precio y condiciones visibles de la suscripcion y el flujo de restauracion.
- El otorgamiento mensual de monedas actual ocurre en JavaScript/localStorage; revisar su persistencia y validacion en servidor antes de vender ese beneficio.
- Completar ficha, capturas, icono, politica de privacidad, seguridad de datos, clasificacion, anuncios y acceso para revision. Revisar eliminacion de cuenta porque el juego ofrece registro.
- Cumplir las pruebas cerradas que Play Console exija para la cuenta.
- No se ha generado ni subido un AAB de publicacion todavia.

Referencias:
- https://www.revenuecat.com/docs/getting-started/entitlements/android-products
- https://www.revenuecat.com/docs/service-credentials/creating-play-service-credentials
- https://developer.android.com/google/play/billing/test
- https://support.google.com/googleplay/android-developer/answer/14151465
