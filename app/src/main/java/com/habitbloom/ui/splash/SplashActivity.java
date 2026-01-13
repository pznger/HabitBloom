package com.habitbloom.ui.splash;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.animation.AlphaAnimation;
import android.view.animation.Animation;

import androidx.appcompat.app.AppCompatActivity;

import com.habitbloom.R;
import com.habitbloom.data.repository.UserRepository;
import com.habitbloom.ui.main.MainActivity;

@SuppressLint("CustomSplashScreen")
public class SplashActivity extends AppCompatActivity {

    private static final long SPLASH_DELAY = 1500;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        // Fade in animation
        AlphaAnimation fadeIn = new AlphaAnimation(0.0f, 1.0f);
        fadeIn.setDuration(500);
        fadeIn.setFillAfter(true);
        
        findViewById(R.id.tv_icon).startAnimation(fadeIn);
        findViewById(R.id.tv_app_name).startAnimation(fadeIn);
        findViewById(R.id.tv_slogan).startAnimation(fadeIn);

        // Initialize user
        UserRepository userRepository = new UserRepository(getApplication());
        userRepository.createUserIfNotExists(() -> {
            // Navigate to main after delay
            new Handler(Looper.getMainLooper()).postDelayed(this::navigateToMain, SPLASH_DELAY);
        });
    }

    private void navigateToMain() {
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
        finish();
        overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
    }
}
