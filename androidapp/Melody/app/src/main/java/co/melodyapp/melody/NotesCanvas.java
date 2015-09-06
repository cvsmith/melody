package co.melodyapp.melody;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.view.View;

import java.util.ArrayList;

public class NotesCanvas extends View {

    private ArrayList<ArrayList<double[]>> notes;
    public int width;
    public int height;
    Context context;

    public NotesCanvas(Context context, AttributeSet attrs, ArrayList<ArrayList<double[]>> notes) {
        super(context, attrs);
        this.context = context;

        this.notes = notes;
    }

    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        Paint mPaint = new Paint();
        mPaint.setAntiAlias(true);
        mPaint.setStyle(Paint.Style.STROKE);
        mPaint.setStrokeJoin(Paint.Join.ROUND);
        mPaint.setStrokeWidth(4f);
        for(int timestep = 0; timestep<notes.size(); timestep++){
            //RED CHANNEL
            mPaint.setColor(Color.RED);
            double[] reds = notes.get(timestep).get(0);
            for(double r: reds){
                canvas.drawLine((float)(timestep*width/48.0), (float) r, (int)((float) (timestep+1)*width/48.0), (float) r, mPaint);
            }
        }
    }
}
