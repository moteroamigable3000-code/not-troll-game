package com.bfjstudios.nottroll.android

import android.app.Activity
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.ActivityCompat
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import java.util.concurrent.TimeUnit

private const val REMINDER_WORK_NAME = "daily_play_reminder"
private const val NOTIFICATION_PERMISSION_REQUEST_CODE = 42

// Runs once a day but lets WorkManager pick the moment inside a flexible
// trailing window, so the reminder doesn't land at the exact same clock time
// every day.
object NotificationScheduler {

    fun schedule(activity: Activity) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU &&
            ActivityCompat.checkSelfPermission(activity, android.Manifest.permission.POST_NOTIFICATIONS)
                != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                activity,
                arrayOf(android.Manifest.permission.POST_NOTIFICATIONS),
                NOTIFICATION_PERMISSION_REQUEST_CODE
            )
        }

        val request = PeriodicWorkRequestBuilder<ReminderWorker>(1, TimeUnit.DAYS, 8, TimeUnit.HOURS)
            .build()
        WorkManager.getInstance(activity).enqueueUniquePeriodicWork(
            REMINDER_WORK_NAME,
            ExistingPeriodicWorkPolicy.KEEP,
            request
        )
    }
}
