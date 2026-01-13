package com.habitbloom.ui.main;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentTransaction;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.habitbloom.R;
import com.habitbloom.ui.garden.GardenFragment;
import com.habitbloom.ui.habit.CreateHabitActivity;
import com.habitbloom.ui.habit.HabitListFragment;
import com.habitbloom.ui.settings.SettingsFragment;
import com.habitbloom.ui.stats.StatsFragment;
import com.habitbloom.utils.Constants;

public class MainActivity extends AppCompatActivity {

    private BottomNavigationView bottomNav;
    private FloatingActionButton fabAddHabit;
    private Fragment currentFragment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initViews();
        setupBottomNavigation();
        setupFab();

        // Default to garden fragment
        if (savedInstanceState == null) {
            loadFragment(new GardenFragment());
            bottomNav.setSelectedItemId(R.id.nav_garden);
        }
    }

    private void initViews() {
        bottomNav = findViewById(R.id.bottom_navigation);
        fabAddHabit = findViewById(R.id.fab_add_habit);
    }

    private void setupBottomNavigation() {
        bottomNav.setOnItemSelectedListener(item -> {
            Fragment fragment = null;
            int itemId = item.getItemId();

            if (itemId == R.id.nav_garden) {
                fragment = new GardenFragment();
                fabAddHabit.setVisibility(View.VISIBLE);
            } else if (itemId == R.id.nav_habits) {
                fragment = new HabitListFragment();
                fabAddHabit.setVisibility(View.VISIBLE);
            } else if (itemId == R.id.nav_stats) {
                fragment = new StatsFragment();
                fabAddHabit.setVisibility(View.GONE);
            } else if (itemId == R.id.nav_settings) {
                fragment = new SettingsFragment();
                fabAddHabit.setVisibility(View.GONE);
            }

            if (fragment != null) {
                loadFragment(fragment);
                return true;
            }
            return false;
        });
    }

    private void setupFab() {
        fabAddHabit.setOnClickListener(v -> {
            Intent intent = new Intent(this, CreateHabitActivity.class);
            startActivityForResult(intent, Constants.REQUEST_CREATE_HABIT);
        });
    }

    private void loadFragment(Fragment fragment) {
        currentFragment = fragment;
        FragmentTransaction transaction = getSupportFragmentManager().beginTransaction();
        transaction.setCustomAnimations(
                android.R.anim.fade_in,
                android.R.anim.fade_out
        );
        transaction.replace(R.id.fragment_container, fragment);
        transaction.commit();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == Constants.REQUEST_CREATE_HABIT && resultCode == RESULT_OK) {
            // Refresh current fragment
            if (currentFragment != null) {
                loadFragment(currentFragment.getClass().equals(GardenFragment.class) 
                        ? new GardenFragment() : new HabitListFragment());
            }
        }
    }
}
