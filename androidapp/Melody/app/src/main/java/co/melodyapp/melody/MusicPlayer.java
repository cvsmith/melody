package co.melodyapp.melody;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;

import com.github.nkzawa.emitter.Emitter;
import com.github.nkzawa.socketio.client.IO;
import com.github.nkzawa.socketio.client.Socket;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;

import co.melodyapp.melody.R;

public class MusicPlayer extends Activity {

    String imageSum;

    private Socket mSocket;
    {
        try {
            mSocket = IO.socket("http://192.168.43.126:8000/");
        } catch (URISyntaxException e) {
            e.printStackTrace();}
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_music_player);

        Intent intent = getIntent();
        imageSum = intent.getStringExtra("co.melodyapp.melody.imagesum");

        //mSocket.connect();
        //mSocket.emit(imageSum, "hi");

        //mSocket.on(imageSum, onMusicNotes);
        //mSocket.connect();

        String jsonObj = "{\"notes\": [ [0, {\"r\": [], \"b\": [], \"g\": []}] , [1, {\"r\": [8], \"b\": [], \"g\": []}] , [2, {\"r\": [8], \"b\": [], \"g\": []}] , [3, {\"r\": [8], \"b\": [], \"g\": []}] , [4, {\"r\": [8], \"b\": [], \"g\": [16]}] , [5, {\"r\": [8], \"b\": [], \"g\": [16]}] , [6, {\"r\": [8], \"b\": [12], \"g\": [16, 18]}] , [7, {\"r\": [8], \"b\": [13], \"g\": [16, 18]}] , [8, {\"r\": [8], \"b\": [], \"g\": [17]}] , [9, {\"r\": [8], \"b\": [], \"g\": [17]}] , [10, {\"r\": [8], \"b\": [], \"g\": []}] , [11, {\"r\": [8], \"b\": [10], \"g\": [15]}] , [12, {\"r\": [], \"b\": [10], \"g\": [15]}] , [13, {\"r\": [3], \"b\": [10], \"g\": [16, 7, 14]}] , [14, {\"r\": [3], \"b\": [11], \"g\": [16, 17, 8, 14]}] , [15, {\"r\": [3], \"b\": [12], \"g\": [8, 17]}] , [16, {\"r\": [3], \"b\": [13], \"g\": [8]}] , [17, {\"r\": [3], \"b\": [14], \"g\": [8]}] , [18, {\"r\": [3], \"b\": [14], \"g\": []}] , [19, {\"r\": [3], \"b\": [14], \"g\": []}] , [20, {\"r\": [3], \"b\": [10], \"g\": []}] , [21, {\"r\": [3], \"b\": [10], \"g\": [16]}] , [22, {\"r\": [7], \"b\": [10], \"g\": [16]}] , [23, {\"r\": [7], \"b\": [11], \"g\": [16, 17]}] , [24, {\"r\": [7], \"b\": [11, 12], \"g\": [15]}] , [25, {\"r\": [8], \"b\": [13], \"g\": [16]}] , [26, {\"r\": [8], \"b\": [13], \"g\": [16]}] , [27, {\"r\": [7], \"b\": [14], \"g\": []}] , [28, {\"r\": [5], \"b\": [14], \"g\": []}] , [29, {\"r\": [4], \"b\": [11], \"g\": [9]}] , [30, {\"r\": [4], \"b\": [11], \"g\": [9, 7]}] , [31, {\"r\": [4], \"b\": [12], \"g\": [16, 8]}] , [32, {\"r\": [4], \"b\": [], \"g\": [16]}] , [33, {\"r\": [10], \"b\": [], \"g\": [16]}] , [34, {\"r\": [10], \"b\": [13], \"g\": [16]}] , [35, {\"r\": [5], \"b\": [14], \"g\": [17]}] , [36, {\"r\": [4], \"b\": [15], \"g\": [8]}] , [37, {\"r\": [4], \"b\": [15], \"g\": [9]}] , [38, {\"r\": [4], \"b\": [12], \"g\": [9]}] , [39, {\"r\": [], \"b\": [12], \"g\": []}] , [40, {\"r\": [5], \"b\": [12], \"g\": []}] , [41, {\"r\": [9, 5], \"b\": [12], \"g\": []}] , [42, {\"r\": [], \"b\": [13], \"g\": []}] , [43, {\"r\": [], \"b\": [13], \"g\": [3]}] , [44, {\"r\": [], \"b\": [14], \"g\": [3, 5]}] , [45, {\"r\": [7], \"b\": [], \"g\": [3, 5]}] , [46, {\"r\": [8], \"b\": [], \"g\": []}] , [47, {\"r\": [], \"b\": [], \"g\": []}] ]}";
        JSONObject jObj = null;
        JSONArray jAr = null;
        ArrayList<ArrayList<double[]>> l = new ArrayList<ArrayList<double[]>>();
        try {
            jObj = new JSONObject(jsonObj);
            jAr = jObj.getJSONArray("notes");
            for(int i=0; i<jAr.length(); i++) {
                JSONArray redArray = jAr.getJSONArray(i).getJSONObject(1).getJSONArray("r");
                double[] reds = new double[redArray.length()];
                for(int r = 0; r<redArray.length(); r++){
                    reds[r] = redArray.getDouble(r);
                }
                JSONArray greenArray = jAr.getJSONArray(i).getJSONObject(1).getJSONArray("g");
                double[] greens = new double[greenArray.length()];
                for(int g = 0; g<greenArray.length(); g++){
                    greens[g] = greenArray.getDouble(g);
                }
                JSONArray blueArray = jAr.getJSONArray(i).getJSONObject(1).getJSONArray("b");
                double[] blues = new double[blueArray.length()];
                for(int b = 0; b<blueArray.length(); b++){
                    blues[b] = blueArray.getDouble(b);
                }

                ArrayList<double[]> list = new ArrayList<double[]>();
                list.add(reds);
                list.add(greens);
                list.add(blues);
                l.add(list);
                //Let the following be a lesson to all past, present and future stubborn idiots who
                //want to implement their own parsers and ignore existing libraries.

                /************************
                String line = jAr.get(i).toString();
                String r = line.substring(line.indexOf("\"r\":[") + 5, line.indexOf("],\"g\""));
                String g = line.substring(line.indexOf("\"g\":[")+5,line.indexOf("],\"b\""));
                String b = line.substring(line.indexOf("\"b\":[")+5,line.indexOf("]}"));
                ArrayList<Double> rVals = new ArrayList<Double>();
                ArrayList<Double> bVals = new ArrayList<Double>();
                ArrayList<Double> gVals = new ArrayList<Double>();

                if(r.length()>0){
                    while(r.indexOf(',')>-1){
                        rVals.add(Double.parseDouble(r.substring(0,r.indexOf(','))));
                        r = r.substring(r.indexOf(',')+1);
                    }
                    rVals.add(Double.parseDouble(r));
                }
                System.out.println("r: " + rVals);
                if(g.length()>0){
                    while(g.indexOf(',')>-1){
                        gVals.add(Double.parseDouble(g.substring(0,g.indexOf(','))));
                        g = g.substring(g.indexOf(',')+1);
                    }
                    gVals.add(Double.parseDouble(g));
                }
                System.out.println("g: " + gVals);
                if(b.length()>0){
                    while(b.indexOf(',')>-1){
                        bVals.add(Double.parseDouble(b.substring(0,b.indexOf(','))));
                        b = b.substring(b.indexOf(',')+1);
                    }
                    bVals.add(Double.parseDouble(b));
                }
                System.out.println("b: " + bVals);
                 *******/

            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private Emitter.Listener onMusicNotes = new Emitter.Listener() {
        @Override
        public void call(final Object... args) {
            MusicPlayer.this.runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    JSONObject data = (JSONObject) args[0];
                    JSONArray notes;
                    try {
                        notes = data.getJSONArray("notes");
                    } catch (JSONException e) {
                        return;
                    }
                    parseNotes(notes);
                }
            });
        }
    };

    public void parseNotes(JSONArray notes)
    {
        ArrayList<ArrayList<double[]>> l = new ArrayList<ArrayList<double[]>>();
    }
}
