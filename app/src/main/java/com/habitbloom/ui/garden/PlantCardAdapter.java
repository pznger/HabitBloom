package com.habitbloom.ui.garden;

import android.graphics.drawable.GradientDrawable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.card.MaterialCardView;
import com.habitbloom.R;
import com.habitbloom.data.database.AppDatabase;
import com.habitbloom.data.database.entity.Habit;
import com.habitbloom.data.database.entity.HabitRecord;
import com.habitbloom.utils.Constants;
import com.habitbloom.utils.DateUtils;

import java.util.ArrayList;
import java.util.List;

public class PlantCardAdapter extends RecyclerView.Adapter<PlantCardAdapter.PlantViewHolder> {

    private List<Habit> habits = new ArrayList<>();
    private final OnPlantClickListener listener;

    public interface OnPlantClickListener {
        void onPlantClick(Habit habit);
    }

    public PlantCardAdapter(OnPlantClickListener listener) {
        this.listener = listener;
    }

    public void setHabits(List<Habit> habits) {
        this.habits = habits;
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public PlantViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_plant_card, parent, false);
        return new PlantViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull PlantViewHolder holder, int position) {
        Habit habit = habits.get(position);
        holder.bind(habit);
    }

    @Override
    public int getItemCount() {
        return habits.size();
    }

    class PlantViewHolder extends RecyclerView.ViewHolder {
        private final MaterialCardView cardPlant;
        private final TextView tvPlantIcon;
        private final TextView tvHabitName;
        private final TextView tvStatus;
        private final ProgressBar progressBar;
        private final ImageView ivCheckStatus;

        PlantViewHolder(@NonNull View itemView) {
            super(itemView);
            cardPlant = itemView.findViewById(R.id.card_plant);
            tvPlantIcon = itemView.findViewById(R.id.tv_plant_icon);
            tvHabitName = itemView.findViewById(R.id.tv_habit_name);
            tvStatus = itemView.findViewById(R.id.tv_status);
            progressBar = itemView.findViewById(R.id.progress_bar);
            ivCheckStatus = itemView.findViewById(R.id.iv_check_status);
        }

        void bind(Habit habit) {
            // Plant icon based on type and growth stage
            String plantIcon = Constants.getPlantIcon(habit.getPlantType(), habit.getGrowthStage());
            tvPlantIcon.setText(plantIcon);

            tvHabitName.setText(habit.getName());

            // Status text
            if (habit.getCurrentStreak() > 0) {
                tvStatus.setText("连续" + habit.getCurrentStreak() + "天");
            } else {
                tvStatus.setText(habit.getGrowthStageName());
            }

            // Progress bar (streak progress to next stage)
            int progress = calculateProgress(habit.getCurrentStreak());
            progressBar.setProgress(progress);

            // Check if completed today
            AppDatabase.databaseExecutor.execute(() -> {
                String today = DateUtils.getTodayString();
                HabitRecord record = AppDatabase.getDatabase(itemView.getContext())
                        .habitRecordDao()
                        .getRecordByHabitAndDate(habit.getHabitId(), today);
                
                boolean isCompletedToday = record != null && record.isCompleted();
                itemView.post(() -> {
                    ivCheckStatus.setVisibility(isCompletedToday ? View.VISIBLE : View.GONE);
                    if (isCompletedToday) {
                        tvStatus.setText("今日已完成");
                    }
                });
            });

            cardPlant.setOnClickListener(v -> {
                if (listener != null) {
                    listener.onPlantClick(habit);
                }
            });
        }

        private int calculateProgress(int streak) {
            // Calculate progress towards next growth stage
            if (streak >= 66) return 100;
            if (streak >= 21) return (int) ((streak - 21) / 45.0 * 100);
            if (streak >= 7) return (int) ((streak - 7) / 14.0 * 100);
            if (streak >= 3) return (int) ((streak - 3) / 4.0 * 100);
            return (int) (streak / 3.0 * 100);
        }
    }
}
