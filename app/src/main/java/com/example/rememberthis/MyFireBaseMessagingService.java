package com.example.rememberthis;

import android.util.Log;
import android.widget.Toast;

import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

public class MyFireBaseMessagingService extends FirebaseMessagingService   {

    // This class handles the override functions for messaging using aws + FCM

    private static final String TAG = "MESSAGE";

    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        Log.d(TAG, "From: " + remoteMessage.getFrom());

        if (remoteMessage.getData().size() > 0) {
            Log.d(TAG, "Message data payload: " + remoteMessage.getData());
        }

        if (remoteMessage.getNotification() != null) {
            Log.d(TAG, "Message Notification Body: " + remoteMessage.getNotification().getBody());
        }
        Toast.makeText(this, (CharSequence) remoteMessage.getData(), Toast.LENGTH_SHORT).show();
//        sendNotification(remoteMessage.getNotification().getBody());

    }

//    private void sendNotification(String messageBody) {
//        Intent intent = new Intent(this, NewActivity.class);
//        intent.putExtra("key", messageBody);
//        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
//        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0 /* Request code */, intent,
//                PendingIntent.FLAG_ONE_SHOT);
//        Bitmap icon2 = BitmapFactory.decodeResource(getResources(),
//                R.mipmap.ic_launcher);
//
//        Uri defaultSoundUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
//        NotificationCompat.Builder notificationBuilder = new NotificationCompat.Builder(this)
//                .setSmallIcon(R.mipmap.ic_launcher)
//                .setContentTitle("FCM Sample")
//                .setContentText(messageBody)
//                .setAutoCancel(true)
//                .setLargeIcon(icon2)
//                .setSound(defaultSoundUri)
//                .setContentIntent(pendingIntent);
//
//        NotificationManager notificationManager =
//                (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
//
//        notificationManager.notify(new Random().nextInt() /* ID of notification */, notificationBuilder.build());
//    }
}
