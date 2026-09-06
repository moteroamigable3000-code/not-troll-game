# Not A Troll Game — libGDX

Port del juego original (Canvas/JS + backend FastAPI) a libGDX, para poder
compilar a PC (LWJGL3), Android (APK / Play Store) y, mas adelante, iOS.

## Estructura

- `core/` — toda la logica del juego (fisica, niveles, menus, sonido). Compartida por todas las plataformas.
- `desktop/` — lanzador de escritorio (Windows/Mac/Linux vía LWJGL3).
- `android/` — lanzador Android.
- `assets/` — imagenes, audio y `levels.json` (los 100 niveles, exportados desde `backend/levels.py`).

## Abrir en Android Studio

1. Abre Android Studio → **Open** → selecciona la carpeta `NotTrollGDX`.
2. Deja que Gradle sincronice (usa el Gradle Wrapper incluido, no hace falta instalar Gradle aparte).
3. Selecciona la configuracion de ejecucion **android** y un emulador o dispositivo conectado, luego Run.
4. Para escritorio, selecciona la configuracion **desktop** (o `gradlew desktop:run` en terminal).

## Compilar por linea de comandos

```powershell
# Windows (usa el JDK de Android Studio si no tienes uno propio)
$env:JAVA_HOME = "C:\Program Files\Android\Android Studio\jbr"

# Jugar en PC
.\gradlew.bat desktop:run

# Generar APK debug (para probar en el celular)
.\gradlew.bat android:assembleDebug
# el APK queda en android/build/outputs/apk/debug/android-debug.apk

# Generar AAB de release (para subir a Play Store) — requiere firmar con tu keystore
.\gradlew.bat android:bundleRelease
```

## Estado actual (v1)

Portado y funcionando:
- Fisica exacta del original (gravedad, salto, coyote time, jump buffer, fricción/hielo, rebote).
- Los 100 niveles, con todas las trampas: picos ocultos, pisos falsos, plataformas
  que se derrumban, sierras, picos de pared, bloques y bombas que caen, teletransportadores,
  muro que persigue (run wall), plataformas moviles.
- Menu principal, mapa de niveles (scrollable, con progreso bloqueado/desbloqueado),
  opciones (sonido/musica), pantalla de info.
  - Progreso guardado localmente en el dispositivo (Preferences), equivalente al
  `localStorage` de la version web.
- Sonido y musica (efectos generados a partir de la sintesis original, musica reusada de `recursos/`).
- Controles: teclado (flechas/WASD + espacio) y tactiles en pantalla (para Android).

Pendiente / simplificado a proposito, para no bloquear esta primera version:
- **Perfil / login en la nube**: la version web permitia iniciar sesion contra el backend
  FastAPI (`backend/`) para sincronizar progreso entre dispositivos. Esta version guarda
  el progreso solo en el dispositivo. Se puede agregar despues con `Gdx.net.HttpRequestBuilder`
  contra el mismo backend.
- **Fidelidad visual**: el juego original dibuja con gradientes/canvas 2D muy detallados
  (portal con espirales, vinetas, texturas). Aqui se aproximan con formas solidas via
  `ShapeRenderer` — el gameplay es identico, el arte es mas simple. Se puede reemplazar
  facilmente por sprites/atlas si se quiere el look exacto.

## Para publicar

- **Play Store**: crear keystore de firma, `android:bundleRelease`, subir el `.aab`
  a Play Console (cuenta de desarrollador, pago unico de 25 USD). `targetSdk` ya
  esta en 36 (vigente para requisitos actuales de Play Store).
- **App Store (iOS)**: libGDX soporta iOS via RoboVM (`gdx-backend-robovm`). Requiere
  Mac + Xcode + cuenta Apple Developer (99 USD/año). No incluido todavia en este
  proyecto — se agrega como modulo `ios/` cuando quieras dar ese paso.
