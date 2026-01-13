package com.habitbloom.ui.stats;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ProgressBar;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.habitbloom.R;
import com.habitbloom.ui.viewmodel.StatsViewModel;

public class StatsFragment extends Fragment {

    private ProgressBar progressMonthly;
    private TextView tvMonthlyRate;
    private TextView tvCurrentStreak;
    private TextView tvLongestStreak;
    private TextView tvTotalHabits;
    private TextView tvTotalCompleted;
    private RecyclerView recyclerAchievements;

    private StatsViewModel statsViewModel;
    private AchievementAdapter achievementAdapter;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_stats, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        initViews(view);
        initViewModel();
        setupRecyclerView();
        observeData();
    }

    private void initViews(View view) {
        progressMonthly = view.findViewById(R.id.progress_monthly);
        tvMonthlyRate = view.findViewById(R.id.tv_monthly_rate);
        tvCurrentStreak = view.findViewById(R.id.tv_current_streak);
        tvLongestStreak = view.findViewById(R.id.tv_longest_streak);
        tvTotalHabits = view.findViewById(R.id.tv_total_habits);
        tvTotalCompleted = view.findViewById(R.id.tv_total_completed);
        recyclerAchievements = view.findViewById(R.id.recycler_achievements);
    }

    private void initViewModel() {
        statsViewModel = new ViewModelProvider(this).get(StatsViewModel.class);
    }

    private void setupRecyclerView() {
        achievementAdapter = new AchievementAdapter();
        recyclerAchievements.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerAchievements.setAdapter(achievementAdapter);
    }

    private void observeData() {
        statsViewModel.getStatsData().observe(getViewLifecycleOwner(), data -> {
            if (data != null) {
                progressMonthly.setProgress(data.monthlyCompletionRate);
                tvMonthlyRate.setText(data.monthlyCompletionRate + "%");
                tvLongestStreak.setText(String.valueOf(data.maxLongestStreak));
                tvTotalHabits.setText(String.valueOf(data.totalHabits));
                tvTotalCompleted.setText(String.valueOf(data.totalCompletedCount));
            }
        });

        statsViewModel.getAllHabits().observe(getViewLifecycleOwner(), habits -> {
            if (habits != null && !habits.isEmpty()) {
                int maxStreak = 0;
                for (var habit : habits) {
                    if (habit.getCurrentStreak() > maxStreak) {
                        maxStreak = habit.getCurrentStreak();
                    }
                }
                tvCurrentStreak.setText(String.valueOf(maxStreak));
            } else {
                tvCurrentStreak.setText("0");
            }
        });

        statsViewModel.getUnlockedAchievements().observe(getViewLifecycleOwner(), achievements -> {
            if (achievements != null) {
                achievementAdapter.setAchievements(achievements);
            }
        });

        // Load stats
        statsViewModel.loadStats();
    }
}
