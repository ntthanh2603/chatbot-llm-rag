import numpy as np
from scipy import stats

# Data for Non-RAG and RAG
non_rag = np.array([0.80, 0.82, 0.76, 0.78, 0.81])  # Non-RAG
rag = np.array([0.85, 0.84, 0.79, 0.81, 0.85])      # RAG

# Difference between RAG and Non-RAG
difference = rag - non_rag

# Perform paired t-test
t_stat, p_value = stats.ttest_1samp(difference, 0)

print(f"T-statistic: {t_stat}")
print(f"P-value: {p_value}")

if p_value < 0.05:
    print("Sự khác biệt có ý nghĩa thống kê!")
else:
    print("Sự khác biệt không có ý nghĩa thống kê.")
