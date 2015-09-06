package co.melodyapp.melody;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.hardware.Camera;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.RelativeLayout;

import com.github.nkzawa.socketio.client.IO;
import com.github.nkzawa.socketio.client.Socket;
import com.squareup.okhttp.MediaType;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.RequestBody;
import com.squareup.okhttp.Response;

import java.io.IOException;
import java.net.URISyntaxException;
import java.net.URL;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class CameraActivity extends Activity {

    private Camera mCamera;

    private byte[] image;

    private Bundle savedState;

    public static final MediaType IMGJPEG = MediaType.parse("image/jpeg");
    OkHttpClient client = new OkHttpClient();


    String post(String url, byte[] img) throws IOException {
        RequestBody body = RequestBody.create(IMGJPEG, img);
        Request request = new Request.Builder()
                .url(url)
                .post(body)
                .build();
        Response response = client.newCall(request).execute();
        return response.body().string();
    }

    /*private Socket mSocket;
    {
        try {
            mSocket = IO.socket("http://192.168.43.126:8000/");
        } catch (URISyntaxException e) {}
    }*/

    private Camera.PictureCallback mPicture = new Camera.PictureCallback() {

        @Override
        public void onPictureTaken(byte[] data, Camera camera) {
            image = data;
            mCamera.startPreview();
            displayTakenImage();
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        savedState = savedInstanceState;
        setContentView(R.layout.activity_camera);

        mCamera = getCameraInstance();
        CameraPreview mPreview = new CameraPreview(this, mCamera);
        FrameLayout preview = (FrameLayout) findViewById(R.id.camera_preview);
        preview.addView(mPreview);
        Button camButton = (Button) findViewById(R.id.camera_button);
        camButton.setOnClickListener(
                new Button.OnClickListener() {
                    public void onClick(View v) {
                        mCamera.takePicture(null, null, mPicture);
                    }
                }
        );
    }

    public static Camera getCameraInstance(){
        Camera camera = null;
        try {
            camera = Camera.open();
            camera.setDisplayOrientation(90);
            Camera.Parameters params = camera.getParameters();
            params.setFlashMode(Camera.Parameters.FLASH_MODE_ON);
            camera.setParameters(params);
        }
        catch(Exception e) {
            Log.d("CAMERA", "Camera instance exception");
        }
        return camera;
    }

    public void displayTakenImage(){
        Bitmap takenPicture = BitmapFactory.decodeByteArray(image, 0, image.length);
        Matrix mat = new Matrix();
        mat.postRotate(90);
        Bitmap rotPicture = Bitmap.createBitmap(takenPicture , 0, 0, takenPicture.getWidth(), takenPicture.getHeight(), mat, true);
        FrameLayout preview = (FrameLayout) findViewById(R.id.camera_preview);
        RelativeLayout blockerBottom = (RelativeLayout) findViewById(R.id.blocker_bottom);
        preview.removeAllViews();
        blockerBottom.removeAllViews();
        View buttonsLayout = getLayoutInflater().inflate(R.layout.picture_buttons, null);
        blockerBottom.addView(buttonsLayout);
        final Button btnSend = (Button) findViewById(R.id.btn_send);
        btnSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                btnSend();
            }
        });
        final Button btnDelete = (Button) findViewById(R.id.btn_delete);
        btnDelete.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                btnDelete();
            }
        });
        ImageView iv = new ImageView(this);
        iv.setImageBitmap(rotPicture);
        preview.addView(iv);
    }

    public void btnSend(){
        Intent intent = new Intent(this, MusicPlayer.class);
        intent.putExtra("co.melodyapp.melody.imagesum", md5(image.toString()));
        POSTTask pT = new POSTTask();
        pT.execute();
        startActivity(intent);
    }

    public void btnDelete(){
        onCreate(savedState);
    }

    public void onResume(){
        super.onResume();
        if(mCamera == null) mCamera = getCameraInstance();
    }

    private class POSTTask extends AsyncTask<URL, Integer, Void> {
        protected Void doInBackground(URL... urls) {
            try {
                post("http://192.168.43.126:8000/", image);
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }

        protected void onPostExecute(Void unused) {
            Log.d("ASYNC TASK", "Done.");
        }
    }

    public String md5( String s) {
        final String MD5 = "MD5";
        try {
            // Create MD5 Hash
            MessageDigest digest = java.security.MessageDigest.getInstance(MD5);
            digest.update(s.getBytes());
            byte messageDigest[] = digest.digest();

            // Create Hex String
            StringBuilder hexString = new StringBuilder();
            for (byte aMessageDigest : messageDigest) {
                String h = Integer.toHexString(0xFF & aMessageDigest);
                while (h.length() < 2)
                    h = "0" + h;
                hexString.append(h);
            }
            return hexString.toString();

        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        return "";
    }
}
