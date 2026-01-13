package com.habitbloom.notification;

import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

import androidx.core.app.NotificationCompat;

import com.habitbloom.R;
import com.habitbloom.ui.main.MainActivity;
import com.habitbloom.utils.Constants;

public class ReminderReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        String habitName = intent.getStringExtra("habit_name");
        long habitId = intent.getLongExtra("habit_id", -1);

        if (habitName == null) {
            habitName = "习惯";
        }

        // Create notification intent
        Intent notificationIntent = new Intent(context, MainActivity.class);
        notificationIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        notificationIntent.putExtra(Constants.EXTRA_FROM_NOTIFICATION, true);
        notificationIntent.putExtra(Constants.EXTRA_HABIT_ID, habitId);

        PendingIntent pendingIntent = PendingIntent.getActivity(
                context,
                (int) habitId,
                notificationIntent,
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
        );

        // Build notification
        NotificationCompat.Builder builder = new NotificationCompat.Builder(context, Constants.CHANNEL_ID_REMINDER)
                .setSmallIcon(R.drawable.ic_notification)
                .setContentTitle(context.getString(R.string.reminder_title))
                .setContentText(context.getString(R.string.reminder_message, habitName))
                .setPriority(NotificationCompat.PRIORITY_DEFAULT)
                .setContentIntent(pendingIntent)
                .setAutoCancel(true);

        // Show notification
        NotificationManager notificationManager = 
                (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
        if (notificationManager != null) {
            notificationManager.notify((int) habitId, builder.build());
        }
    }
}
