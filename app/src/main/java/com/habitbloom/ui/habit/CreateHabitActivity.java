package com.habitbloom.ui.habit;

import android.app.TimePickerDialog;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.chip.Chip;
import com.google.android.material.chip.ChipGroup;
import com.google.android.material.slider.Slider;
import com.google.android.material.switchmaterial.SwitchMaterial;
import com.google.android.material.textfield.TextInputEditText;
import com.habitbloom.R;
import com.habitbloom.data.database.entity.Habit;
import com.habitbloom.data.database.entity.Reminder;
import com.habitbloom.ui.viewmodel.HabitViewModel;
import com.habitbloom.utils.Constants;

import java.util.Locale;

public class CreateHabitActivity extends AppCompatActivity implements IconAdapter.OnIconClickListener {

    private TextInputEditText etHabitName;
    private ChipGroup chipGroupCategory;
    private ChipGroup chipGroupPlant;
    private RecyclerView recyclerIcons;
    private Slider sliderFrequency;
    private Slider sliderDifficulty;
    private TextView tvFrequency;
    private TextView tvDifficulty;
    private TextView tvReminderTime;
    private SwitchMaterial switchReminder;
    private Button btnSave;

    private HabitViewModel habitViewModel;
    private IconAdapter iconAdapter;
    private String selectedIcon = "🌱";
    private int reminderHour = 8;
    private int reminderMinute = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_habit);

        initViews();
        initViewModel();
        setupToolbar();
        setupIconSelector();
        setupSliders();
        setupReminderTime();
        setupSaveButton();
    }

    private void initViews() {
        etHabitName = findViewById(R.id.et_habit_name);
        chipGroupCategory = findViewById(R.id.chip_group_category);
        chipGroupPlant = findViewById(R.id.chip_group_plant);
        recyclerIcons = findViewById(R.id.recycler_icons);
        sliderFrequency = findViewById(R.id.slider_frequency);
        sliderDifficulty = findViewById(R.id.slider_difficulty);
        tvFrequency = findViewById(R.id.tv_frequency);
        tvDifficulty = findViewById(R.id.tv_difficulty);
        tvReminderTime = findViewById(R.id.tv_reminder_time);
        switchReminder = findViewById(R.id.switch_reminder);
        btnSave = findViewById(R.id.btn_save);
    }

    private void initViewModel() {
        habitViewModel = new ViewModelProvider(this).get(HabitViewModel.class);
    }

    private void setupToolbar() {
        Toolbar toolbar = findViewById(R.id.toolbar);
        toolbar.setNavigationOnClickListener(v -> finish());
    }

    private void setupIconSelector() {
        iconAdapter = new IconAdapter(Constants.HABIT_ICONS, this);
        recyclerIcons.setLayoutManager(new GridLayoutManager(this, 8));
        recyclerIcons.setAdapter(iconAdapter);
    }

    private void setupSliders() {
        // Frequency slider
        sliderFrequency.addOnChangeListener((slider, value, fromUser) -> {
            tvFrequency.setText((int) value + "次/周");
        });
        tvFrequency.setText("5次/周");

        // Difficulty slider
        sliderDifficulty.addOnChangeListener((slider, value, fromUser) -> {
            int level = (int) value;
            StringBuilder stars = new StringBuilder();
            for (int i = 0; i < 5; i++) {
                stars.append(i < level ? "★" : "☆");
            }
            tvDifficulty.setText(stars.toString());
        });
        tvDifficulty.setText("★★★☆☆");
    }

    private void setupReminderTime() {
        tvReminderTime.setText(String.format(Locale.getDefault(), "%02d:%02d", reminderHour, reminderMinute));
        
        tvReminderTime.setOnClickListener(v -> {
            TimePickerDialog dialog = new TimePickerDialog(this,
                    (view, hourOfDay, minute) -> {
                        reminderHour = hourOfDay;
                        reminderMinute = minute;
                        tvReminderTime.setText(String.format(Locale.getDefault(), "%02d:%02d", hourOfDay, minute));
                    },
                    reminderHour, reminderMinute, true);
            dialog.show();
        });
    }

    private void setupSaveButton() {
        btnSave.setOnClickListener(v -> saveHabit());
    }

    private void saveHabit() {
        String name = etHabitName.getText() != null ? etHabitName.getText().toString().trim() : "";
        
        if (name.isEmpty()) {
            etHabitName.setError(getString(R.string.field_required));
            return;
        }

        // Get selected category
        String category = getSelectedCategory();
        
        // Get selected plant type
        String plantType = getSelectedPlantType();

        // Create habit
        Habit habit = new Habit();
        habit.setName(name);
        habit.setCategory(category);
        habit.setPlantType(plantType);
        habit.setIcon(selectedIcon);
        habit.setTargetFrequency((int) sliderFrequency.getValue());
        habit.setDifficulty((int) sliderDifficulty.getValue());

        habitViewModel.createHabit(habit);

        Toast.makeText(this, R.string.habit_created, Toast.LENGTH_SHORT).show();
        setResult(RESULT_OK);
        finish();
    }

    private String getSelectedCategory() {
        int checkedId = chipGroupCategory.getCheckedChipId();
        if (checkedId == R.id.chip_health) return Constants.CATEGORY_HEALTH;
        if (checkedId == R.id.chip_study) return Constants.CATEGORY_STUDY;
        if (checkedId == R.id.chip_work) return Constants.CATEGORY_WORK;
        return Constants.CATEGORY_LIFE;
    }

    private String getSelectedPlantType() {
        int checkedId = chipGroupPlant.getCheckedChipId();
        if (checkedId == R.id.chip_flower) return Constants.PLANT_FLOWER;
        if (checkedId == R.id.chip_tree) return Constants.PLANT_TREE;
        if (checkedId == R.id.chip_cactus) return Constants.PLANT_CACTUS;
        return Constants.PLANT_HERB;
    }

    @Override
    public void onIconClick(String icon) {
        selectedIcon = icon;
    }
}
