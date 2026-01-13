package com.habitbloom.ui.habit;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.textfield.TextInputEditText;
import com.habitbloom.R;
import com.habitbloom.data.database.entity.Habit;
import com.habitbloom.ui.viewmodel.HabitViewModel;
import com.habitbloom.utils.Constants;
import com.habitbloom.utils.DateUtils;

public class HabitDetailActivity extends AppCompatActivity {

    private TextView tvPlantIcon;
    private TextView tvHabitName;
    private TextView tvCategory;
    private ProgressBar progressGrowth;
    private TextView tvGrowthStage;
    private TextView tvStreak;
    private TextView tvTarget;
    private TextView tvMonthly;
    private RecyclerView recyclerCalendar;
    private Button btnCheckIn;
    private Button btnAddNote;

    private HabitViewModel habitViewModel;
    private long habitId;
    private Habit currentHabit;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_habit_detail);

        habitId = getIntent().getLongExtra(Constants.EXTRA_HABIT_ID, -1);
        if (habitId == -1) {
            finish();
            return;
        }

        initViews();
        initViewModel();
        setupToolbar();
        observeData();
        setupButtons();
    }

    private void initViews() {
        tvPlantIcon = findViewById(R.id.tv_plant_icon);
        tvHabitName = findViewById(R.id.tv_habit_name);
        tvCategory = findViewById(R.id.tv_category);
        progressGrowth = findViewById(R.id.progress_growth);
        tvGrowthStage = findViewById(R.id.tv_growth_stage);
        tvStreak = findViewById(R.id.tv_streak);
        tvTarget = findViewById(R.id.tv_target);
        tvMonthly = findViewById(R.id.tv_monthly);
        recyclerCalendar = findViewById(R.id.recycler_calendar);
        btnCheckIn = findViewById(R.id.btn_check_in);
        btnAddNote = findViewById(R.id.btn_add_note);
    }

    private void initViewModel() {
        habitViewModel = new ViewModelProvider(this).get(HabitViewModel.class);
    }

    private void setupToolbar() {
        Toolbar toolbar = findViewById(R.id.toolbar);
        toolbar.setNavigationOnClickListener(v -> finish());

        ImageButton btnEdit = findViewById(R.id.btn_edit);
        btnEdit.setOnClickListener(v -> {
            // TODO: Open edit activity
            Toast.makeText(this, "编辑功能开发中", Toast.LENGTH_SHORT).show();
        });
    }

    private void observeData() {
        habitViewModel.getHabitById(habitId).observe(this, habit -> {
            if (habit != null) {
                currentHabit = habit;
                updateUI(habit);
            }
        });

        habitViewModel.getCheckInResult().observe(this, result -> {
            if (result != null && result.success) {
                Toast.makeText(this, "🎉 打卡成功！连续" + result.newStreak + "天", Toast.LENGTH_SHORT).show();
                // Update button state
                btnCheckIn.setEnabled(false);
                btnCheckIn.setText("✅ 今日已完成");
            }
        });

        habitViewModel.getToastMessage().observe(this, message -> {
            if (message != null && !message.isEmpty()) {
                Toast.makeText(this, message, Toast.LENGTH_LONG).show();
            }
        });
    }

    private void updateUI(Habit habit) {
        String plantIcon = Constants.getPlantIcon(habit.getPlantType(), habit.getGrowthStage());
        tvPlantIcon.setText(plantIcon);
        tvHabitName.setText(habit.getName());
        tvCategory.setText(Constants.getCategoryIcon(habit.getCategory()) + " " + 
                Constants.getCategoryName(habit.getCategory()));

        // Growth progress
        int progress = calculateGrowthProgress(habit.getCurrentStreak());
        progressGrowth.setProgress(progress);
        tvGrowthStage.setText(habit.getGrowthStageName());

        // Stats
        tvStreak.setText(habit.getCurrentStreak() + "天");
        tvTarget.setText(habit.getTargetFrequency() + "次");
        
        // Calculate monthly completed
        String monthStart = DateUtils.getMonthStartDate();
        String monthEnd = DateUtils.getMonthEndDate();
        // For now just show a placeholder, actual calculation needs async
        tvMonthly.setText("--/" + DateUtils.getDayOfMonth());

        // Setup calendar
        setupCalendar();

        // Check if already completed today
        checkTodayStatus();
    }

    private int calculateGrowthProgress(int streak) {
        if (streak >= 66) return 100;
        if (streak >= 21) return 75 + (int) ((streak - 21) / 45.0 * 25);
        if (streak >= 7) return 50 + (int) ((streak - 7) / 14.0 * 25);
        if (streak >= 3) return 25 + (int) ((streak - 3) / 4.0 * 25);
        return (int) (streak / 3.0 * 25);
    }

    private void setupCalendar() {
        CalendarAdapter adapter = new CalendarAdapter(habitId);
        recyclerCalendar.setLayoutManager(new GridLayoutManager(this, 7));
        recyclerCalendar.setAdapter(adapter);
    }

    private void checkTodayStatus() {
        // Check if already completed today in background
        com.habitbloom.data.database.AppDatabase.databaseExecutor.execute(() -> {
            String today = DateUtils.getTodayString();
            boolean isCompleted = com.habitbloom.data.database.AppDatabase.getDatabase(this)
                    .habitRecordDao()
                    .isCompletedToday(habitId, today);
            
            runOnUiThread(() -> {
                if (isCompleted) {
                    btnCheckIn.setEnabled(false);
                    btnCheckIn.setText("✅ 今日已完成");
                } else {
                    btnCheckIn.setEnabled(true);
                    btnCheckIn.setText("🎉  今日打卡");
                }
            });
        });
    }

    private void setupButtons() {
        btnCheckIn.setOnClickListener(v -> {
            habitViewModel.checkIn(habitId, null);
        });

        btnAddNote.setOnClickListener(v -> showNoteDialog());
    }

    private void showNoteDialog() {
        View dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_note, null);
        TextInputEditText etNote = dialogView.findViewById(R.id.et_note);

        new AlertDialog.Builder(this)
                .setView(dialogView)
                .setPositiveButton(R.string.save, (dialog, which) -> {
                    String note = etNote.getText() != null ? etNote.getText().toString() : "";
                    if (!note.isEmpty()) {
                        habitViewModel.checkIn(habitId, note);
                    }
                })
                .setNegativeButton(R.string.cancel, null)
                .show();
    }
}
