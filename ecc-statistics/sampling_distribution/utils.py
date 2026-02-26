import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

np.random.seed(42)

def fair_die_means(n_samples, sample_size, population):
    sample_means = [np.mean(np.random.choice(population, size=sample_size)) for _ in range(n_samples)]

    plt.figure(figsize=(12, 6))
    sns.histplot(x=sample_means, bins=25, binrange=(1,6.0001), color='red')
    plt.axvline(np.mean(sample_means), color='green', linestyle='dashed')
    plt.title("Distribution of Sample Means (n=5 die rolls)")
    plt.xlabel("Sample Means")
    plt.ylabel("Frequency")
    
    plt.text(np.mean(sample_means)+0.15, 990, f"Mean: {np.mean(sample_means):.2f}", color='green')
    plt.text(4.5, 825, "Approximately\nnormal", fontsize=24, color='black')
    plt.show()

def fair_die_variances(n_samples, sample_size, population):
    sample_variances = [np.var(np.random.choice(population, size=sample_size), ddof=1) for _ in range(n_samples)]

    plt.figure(figsize=(12, 6))
    sns.histplot(x=sample_variances, bins=15, color='red', edgecolor='black', stat='frequency')
    plt.axvline(np.mean(sample_variances), color='green', linestyle='dashed')
    plt.title("Distribution of Sample Variances (n=5 die rolls)")
    plt.xlabel("Sample Variances")
    plt.ylabel("Frequency")
    
    plt.text(np.mean(sample_variances)+0.2, 2500, f"Mean: {np.mean(sample_variances):.2f}", color='green')
    plt.text(6, 2300, "Skewed", fontsize=24, color='black')
    plt.show()

def fair_die_proportions(n_samples, sample_size, population):
    sample_proportions = [np.sum(np.random.choice(population, size=sample_size) % 2 == 1) / sample_size for _ in range(n_samples)]

    plt.figure(figsize=(12, 6))
    sns.histplot(x=sample_proportions, bins=6, color='red', edgecolor='black', stat='frequency')
    plt.axvline(np.mean(sample_proportions), color='green', linestyle='dashed')
    plt.title("Distribution of Sample Proportions (n=5 die rolls)")
    plt.xlabel("Sample Proportions")
    plt.ylabel("Frequency")
    
    plt.text(np.mean(sample_proportions)+0.02, 18800, f"Mean: {np.mean(sample_proportions):.3f}", color='green')
    plt.text(0.75, 15000, "Approximately\nnormal", fontsize=20, color='black')
    plt.show()

def mean_range_tables(calculate_mean, calculate_range, calculate_probability):
    ages = [56, 49, 59, 46]
    all_samples = []
    for age1 in ages:
        for age2 in ages:
            all_samples.append([age1, age2])
    
    print("Calculated Sample Means and Ranges:")
    sample_means = []
    sample_ranges = []
    
    for sample in all_samples:
        age1 = sample[0]
        age2 = sample[1]
        mean_result = calculate_mean(age1, age2)
        range_result = calculate_range(age1, age2)
        sample_means.append(mean_result)
        sample_ranges.append(range_result)
        print(f"Sample: {sample}, Mean: {mean_result}, Range: {range_result}")
    
    print('\n')
    print("---Probability Distribution of Sample Mean ---")
    mean_counts = Counter(sample_means)
    total_samples = len(all_samples)
    
    print("| Sample Mean (x̄) | Frequency | Probability P(x̄) |")
    print("|-----------------+-----------+------------------|")
    for mean_val in sorted(mean_counts.keys()):
        frequency = mean_counts[mean_val]
        probability = calculate_probability(frequency, total_samples)
        print(f"| {mean_val:<15.2f} | {frequency:<9} | {probability:<16.4f} |")
    print(f"Mean of Sample Means: {np.mean(sample_means)}")
    
    print('\n')
    print("--- Probability Distribution of Sample Range ---")
    range_counts = Counter(sample_ranges)
    
    print("| Sample Range (R) | Frequency | Probability P(R) |")
    print("|------------------+-----------+------------------|")
    for range_val in sorted(range_counts.keys()):
        frequency = range_counts[range_val]
        probability = frequency / total_samples
        print(f"| {range_val:<16.2f} | {frequency:<9} | {probability:<16.4f} |")
    print(f"Mean of Sample Ranges: {np.mean(sample_ranges)}")