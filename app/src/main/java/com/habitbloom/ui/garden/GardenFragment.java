package com.habitbloom.ui.garden;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.habitbloom.R;
import com.habitbloom.data.database.entity.Habit;
import com.habitbloom.ui.habit.CreateHabitActivity;
import com.habitbloom.ui.habit.HabitDetailActivity;
import com.habitbloom.ui.viewmodel.HabitViewModel;
import com.habitbloom.ui.viewmodel.UserViewModel;
import com.habitbloom.utils.Constants;
import com.habitbloom.utils.DateUtils;

import java.util.Date;

public class GardenFragment extends Fragment implements PlantCardAdapter.OnPlantClickListener {

    private RecyclerView recyclerHabits;
    private LinearLayout emptyState;
    private TextView tvGreeting;
    private TextView tvDate;
    private TextView tvUsername;
    private TextView tvHabitCount;
    private Button btnAddFirstHabit;

    private HabitViewModel habitViewModel;
    private UserViewModel userViewModel;
    private PlantCardAdapter adapter;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_garden, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        
        initViews(view);
        initViewModels();
        setupRecyclerView();
        observeData();
        setupHeader();
    }

    private void initViews(View view) {
        recyclerHabits = view.findViewById(R.id.recycler_habits);
        emptyState = view.findViewById(R.id.empty_state);
        tvGreeting = view.findViewById(R.id.tv_greeting);
        tvDate = view.findViewById(R.id.tv_date);
        tvUsername = view.findViewById(R.id.tv_username);
        tvHabitCount = view.findViewById(R.id.tv_habit_count);
        btnAddFirstHabit = view.findViewById(R.id.btn_add_first_habit);

        btnAddFirstHabit.setOnClickListener(v -> {
            Intent intent = new Intent(getActivity(), CreateHabitActivity.class);
            startActivityForResult(intent, Constants.REQUEST_CREATE_HABIT);
        });
    }

    private void initViewModels() {
        habitViewModel = new ViewModelProvider(this).get(HabitViewModel.class);
        userViewModel = new ViewModelProvider(this).get(UserViewModel.class);
    }

    private void setupRecyclerView() {
        adapter = new PlantCardAdapter(this);
        recyclerHabits.setLayoutManager(new GridLayoutManager(getContext(), 2));
        recyclerHabits.setAdapter(adapter);
    }

    private void observeData() {
        habitViewModel.getAllActiveHabits().observe(getViewLifecycleOwner(), habits -> {
            if (habits != null && !habits.isEmpty()) {
                adapter.setHabits(habits);
                recyclerHabits.setVisibility(View.VISIBLE);
                emptyState.setVisibility(View.GONE);
                tvHabitCount.setText(habits.size() + "个习惯");
            } else {
                recyclerHabits.setVisibility(View.GONE);
                emptyState.setVisibility(View.VISIBLE);
                tvHabitCount.setText("0个习惯");
            }
        });

        userViewModel.getCurrentUser().observe(getViewLifecycleOwner(), user -> {
            if (user != null) {
                tvUsername.setText(user.getUsername());
            }
        });
    }

    private void setupHeader() {
        tvGreeting.setText(DateUtils.getGreeting());
        tvDate.setText(DateUtils.formatDisplayDateFull(new Date()));
    }

    @Override
    public void onPlantClick(Habit habit) {
        Intent intent = new Intent(getActivity(), HabitDetailActivity.class);
        intent.putExtra(Constants.EXTRA_HABIT_ID, habit.getHabitId());
        startActivity(intent);
    }
}
