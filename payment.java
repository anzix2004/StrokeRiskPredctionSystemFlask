package com.example.pet_care;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.example.pet_care.JsonResponse;
import com.razorpay.Checkout;
import com.razorpay.PaymentResultListener;

import org.json.JSONObject;

public class User_payment extends AppCompatActivity implements PaymentResultListener, JsonResponse {

    Button b1;
    SharedPreferences sh;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_user_payment);

        sh= PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

        b1=findViewById(R.id.btn_pay);
        b1.setOnClickListener(v -> {



            startPayment();
        });

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        // Initialize Razorpay Checkout
        Checkout.preload(getApplicationContext());

        // Start payment process
//        startPayment();
    }

    private void startPayment() {
        Checkout checkout = new Checkout();
        checkout.setKeyID("rzp_test_edrzdb8Gbx5U5M");

        // Set up payment details
        try {
            JSONObject options = new JSONObject();
            options.put("name", "Pet Connect");
//            options.put("description", "Payment for your order");
//            options.put("currency", "INR");
//            options.put("amount", Integer.parseInt(Cart.tot) * 100); // Convert to integer and multiply
//            options.put("prefill.email", "test@example.com");
//            options.put("prefill.contact", "9400278981");

            // Open Razorpay Checkout activity
            checkout.open(this, options);
        } catch (Exception e) {
            Toast.makeText(this, "Error in starting payment: " + e.getMessage(), Toast.LENGTH_SHORT).show();
            e.printStackTrace();
        }
    }

    @Override
    public void onPaymentSuccess(String razorpayPaymentId) {
//        Toast.makeText(this, "Payment successful: " + razorpayPaymentId, Toast.LENGTH_LONG).show();

        JsonReq JR=new JsonReq();
        JR.json_response=(JsonResponse) User_payment.this;
        String q="/pet_payment?id="  + sh.getString("lid","")+"&amount="+User_View_Pet_Cart.totalAmount+"&pmid="+User_View_Pet_Cart.selectedPmid;
        q=q.replace(" ","%20");
        JR.execute(q);


        // Handle successful payment here (e.g., update backend, show confirmation, etc.)
    }

    @Override
    public void onPaymentError(int code, String description) {
        Toast.makeText(this, "Payment failed: " + description, Toast.LENGTH_LONG).show();
        // Handle failed payment here (e.g., show error message, retry, etc.)
    }



    @Override
    public void response(JSONObject jo) {
        try {
            String method = jo.getString("method");
            if (method.equalsIgnoreCase("user_pay")) {
                String status = jo.getString("status");
                Log.d("pearl", status);
                if (status.equalsIgnoreCase("success")) {

//                    Toast.makeText(getApplicationContext(), "Success", Toast.LENGTH_LONG).show();
                    startActivity(new Intent(getApplicationContext(),User_Home.class));
                }

                else

                {
                    Toast.makeText(getApplicationContext(), "Failed!!", Toast.LENGTH_LONG).show();

                }
            }


        }catch(Exception e)
        {
            Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_LONG).show();
        }



    }

    @Override
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {

    }


}