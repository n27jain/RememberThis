package com.example.rememberthis;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.VideoView;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.inappmessaging.FirebaseInAppMessaging;
import com.google.firebase.messaging.FirebaseMessaging;
import com.google.firebase.messaging.RemoteMessage;

import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferListener;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferObserver;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferState;
import com.amazonaws.mobileconnectors.s3.transferutility.TransferUtility;
import com.amazonaws.services.s3.AmazonS3Client;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;


public class MainActivity extends AppCompatActivity {

    private ProgressBar progressBar;
    private ImageButton recordButton;
    private ImageButton historyButton ;
    private TextView progressText;


    static final int REQUEST_VIDEO_CAPTURE = 1;
    String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        recordButton =  findViewById(R.id.recordButton);
        historyButton =  findViewById(R.id.historyButton);
        progressBar = findViewById(R.id.progressBar);
        progressText = findViewById(R.id.progressText);
        recordButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                dispatchTakeVideoIntent();
            }
        });

        getInstanceID();

    }




    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent intent) {
        super.onActivityResult(requestCode, resultCode, intent);
        if (requestCode == REQUEST_VIDEO_CAPTURE && resultCode == RESULT_OK) {
            Uri videoUri = intent.getData();
            VideoView videoView =  findViewById(R.id.videoView);
            videoView.setVideoURI(videoUri);
            try {
                InputStream inputStream =  getContentResolver().openInputStream(videoUri);
                uploadWithTransferUtility(inputStream);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }


    public void uploadWithTransferUtility(InputStream video) throws IOException {


        final File tempFile = File.createTempFile("video-", ".mp4", getApplicationContext().getCacheDir());
        OutputStream outStream = new FileOutputStream(tempFile);
        byte[] buffer = new byte[8192];
        int length;
        while ((length = video.read(buffer)) > 0) {
            outStream.write(buffer, 0 ,length);
        }

        String access_key = getString(R.string.access_key);
        String secret_key = getString(R.string.secret_key);
        String bucket_name = getString(R.string.bucket_name);

        AmazonS3Client s3Client = new AmazonS3Client(
                new BasicAWSCredentials(access_key, secret_key)
        );
        TransferUtility transferUtility = TransferUtility.builder().s3Client(s3Client).context(getApplicationContext()).build();

        final TransferObserver observer = transferUtility.upload(bucket_name, tempFile.getName(), tempFile);

        // Attach a listener to the observer to get state update and progress notifications
        observer.setTransferListener(new TransferListener() {

            @Override
            public void onStateChanged(int id, TransferState state) {
                if (TransferState.COMPLETED == state) {
                    Log.d("YourActivity", "Bytes Total: " + observer.getBytesTotal());
                    progressBar.setVisibility(View.GONE);
                    progressText.setVisibility(View.GONE);
                    recordButton.setVisibility(View.VISIBLE);

                }
            }

            @Override
            public void onProgressChanged(int id, long bytesCurrent, long bytesTotal) {
                progressBar.setVisibility(View.VISIBLE);
                progressText.setVisibility(View.VISIBLE);
                recordButton.setVisibility(View.INVISIBLE);

                float percentDonef = ((float) bytesCurrent / (float) bytesTotal) * 100;
                int percentDone = (int)percentDonef;
                progressBar.setProgress(percentDone);
                progressText.setText("Progress:    " + percentDone+ " %");
                Log.d("YourActivity", "ID:" + id + " bytesCurrent: " + bytesCurrent
                        + " bytesTotal: " + bytesTotal + " " + percentDone + "%");
            }

            @Override
            public void onError(int id, Exception ex) {
                tempFile.delete();
            }

        });
    }


    private void dispatchTakeVideoIntent() {
        Intent takeVideoIntent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
        if (takeVideoIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(takeVideoIntent, REQUEST_VIDEO_CAPTURE);
        }
    }

    public void getInstanceID(){

        FirebaseMessaging.getInstance().getToken()
                .addOnCompleteListener(new OnCompleteListener<String>() {
                    @Override
                    public void onComplete(@NonNull Task<String> task) {
                        if (!task.isSuccessful()) {
                            Log.w(TAG, "Fetching FCM registration token failed", task.getException());
                            return;
                        }

                        // Get new FCM registration token
                        String token = task.getResult();

                        Log.d("TOKEN", token);
                        Toast.makeText(MainActivity.this, token, Toast.LENGTH_SHORT).show();
                    }
                });


        // [END log_reg_token]
    }

}
