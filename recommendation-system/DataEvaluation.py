from PreparationData import films
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
sns.set_theme(style='whitegrid')
sns.boxplot(x='vote_average', data=films, showfliers=False)
plt.xlabel("Кол-во рейтингов")
plt.title("Частота рейтингов фильмов")
plt.show()

plt.figure(figsize=(10,5))
sns.set_theme(style='whitegrid')
sns.boxplot(x='vote_count', data=films, showfliers=False)
plt.xlabel("Кол-во оценок")
plt.title("Частота оценок фильмов")
plt.show()




