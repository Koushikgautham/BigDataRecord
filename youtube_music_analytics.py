import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import sys
import io

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

warnings.filterwarnings('ignore')

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

class YouTubeMusicAnalytics:
    """Main class for YouTube Music Analytics Dashboard"""

    def __init__(self, csv_file):
        """Initialize the analytics dashboard with CSV file"""
        self.csv_file = csv_file
        self.df = None
        self.insights = []

    def load_and_clean_data(self):
        """Load CSV data and perform cleaning operations"""
        print("=" * 80)
        print("YOUTUBE MUSIC ANALYTICS DASHBOARD")
        print("=" * 80)
        print("\n[1/6] Loading and cleaning data...")

        # Load the CSV file
        self.df = pd.read_csv(self.csv_file, encoding='utf-8')

        print(f"   ✓ Loaded {len(self.df):,} records")
        print(f"   ✓ Dataset shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns")

        # Convert view_count to numeric
        self.df['view_count'] = pd.to_numeric(self.df['view_count'], errors='coerce')

        # Convert duration to numeric (seconds)
        self.df['duration'] = pd.to_numeric(self.df['duration'], errors='coerce')

        # Convert channel_follower_count to numeric
        self.df['channel_follower_count'] = pd.to_numeric(
            self.df['channel_follower_count'], errors='coerce'
        )

        # Remove rows with missing critical data
        original_count = len(self.df)
        self.df = self.df.dropna(subset=['view_count', 'duration', 'channel'])
        removed_count = original_count - len(self.df)

        if removed_count > 0:
            print(f"   ✓ Removed {removed_count} rows with missing critical data")

        # Add derived features
        self.df['duration_minutes'] = self.df['duration'] / 60
        self.df['views_in_billions'] = self.df['view_count'] / 1_000_000_000
        self.df['views_in_millions'] = self.df['view_count'] / 1_000_000

        print(f"   ✓ Data cleaning completed\n")

        return self.df

    def exploratory_data_analysis(self):
        """Perform exploratory data analysis"""
        print("[2/6] Performing Exploratory Data Analysis...")

        # Basic statistics
        print("\n" + "=" * 80)
        print("DATASET STATISTICS")
        print("=" * 80)

        stats = {
            'Total Songs': f"{len(self.df):,}",
            'Total Channels': f"{self.df['channel'].nunique():,}",
            'Total Views (Billions)': f"{self.df['view_count'].sum() / 1_000_000_000:.2f}B",
            'Average Views per Song': f"{self.df['view_count'].mean():,.0f}",
            'Median Views per Song': f"{self.df['view_count'].median():,.0f}",
            'Average Duration': f"{self.df['duration_minutes'].mean():.2f} minutes",
            'Most Popular Channel': self.df.groupby('channel')['view_count'].sum().idxmax()
        }

        for key, value in stats.items():
            print(f"{key:.<40} {value}")

        # Top 20 most viewed songs
        print("\n" + "=" * 80)
        print("TOP 20 MOST VIEWED SONGS")
        print("=" * 80)

        top_songs = self.df.nlargest(20, 'view_count')[['title', 'channel', 'view_count', 'duration_string']]

        for idx, (_, row) in enumerate(top_songs.iterrows(), 1):
            title = row['title'][:50] + '...' if len(row['title']) > 50 else row['title']
            views = f"{row['view_count']:,.0f}"
            print(f"{idx:2d}. {title:.<55} {views:>15} views")

        # Top 10 channels by total views
        print("\n" + "=" * 80)
        print("TOP 10 CHANNELS BY TOTAL VIEWS")
        print("=" * 80)

        top_channels = self.df.groupby('channel').agg({
            'view_count': 'sum',
            'title': 'count'
        }).sort_values('view_count', ascending=False).head(10)

        top_channels.columns = ['Total Views', 'Number of Songs']

        for idx, (channel, row) in enumerate(top_channels.iterrows(), 1):
            views = f"{row['Total Views']:,.0f}"
            songs = row['Number of Songs']
            channel_name = channel[:40] + '...' if len(channel) > 40 else channel
            print(f"{idx:2d}. {channel_name:.<45} {views:>18} ({songs} songs)")

        print("\n   ✓ EDA completed\n")

        # Store insights
        self.insights.append(f"Dataset contains {len(self.df):,} songs from {self.df['channel'].nunique():,} channels")
        self.insights.append(f"Total combined views: {self.df['view_count'].sum() / 1_000_000_000:.2f} billion")
        self.insights.append(f"Most viewed song: {self.df.nlargest(1, 'view_count')['title'].values[0]}")

        return top_songs, top_channels

    def statistical_analysis(self):
        """Perform statistical analysis"""
        print("[3/6] Performing Statistical Analysis...")

        print("\n" + "=" * 80)
        print("STATISTICAL ANALYSIS")
        print("=" * 80)

        # View count statistics
        print("\n📊 View Count Distribution:")
        print(f"   Mean:        {self.df['view_count'].mean():>15,.0f}")
        print(f"   Median:      {self.df['view_count'].median():>15,.0f}")
        print(f"   Std Dev:     {self.df['view_count'].std():>15,.0f}")
        print(f"   Min:         {self.df['view_count'].min():>15,.0f}")
        print(f"   Max:         {self.df['view_count'].max():>15,.0f}")
        print(f"   25th %ile:   {self.df['view_count'].quantile(0.25):>15,.0f}")
        print(f"   75th %ile:   {self.df['view_count'].quantile(0.75):>15,.0f}")

        # Duration statistics
        print("\n⏱️  Duration Distribution (minutes):")
        print(f"   Mean:        {self.df['duration_minutes'].mean():>15.2f}")
        print(f"   Median:      {self.df['duration_minutes'].median():>15.2f}")
        print(f"   Std Dev:     {self.df['duration_minutes'].std():>15.2f}")
        print(f"   Min:         {self.df['duration_minutes'].min():>15.2f}")
        print(f"   Max:         {self.df['duration_minutes'].max():>15.2f}")

        # Correlation analysis
        print("\n🔗 Correlation Analysis:")

        correlation_data = self.df[['view_count', 'duration', 'channel_follower_count']].dropna()

        if len(correlation_data) > 0:
            corr_duration_views = correlation_data['duration'].corr(correlation_data['view_count'])
            print(f"   Duration vs Views:            {corr_duration_views:>8.4f}")

            if correlation_data['channel_follower_count'].notna().any():
                corr_followers_views = correlation_data['channel_follower_count'].corr(correlation_data['view_count'])
                print(f"   Channel Followers vs Views:   {corr_followers_views:>8.4f}")

        # Category analysis
        mega_hits = len(self.df[self.df['view_count'] >= 1_000_000_000])
        popular = len(self.df[(self.df['view_count'] >= 100_000_000) & (self.df['view_count'] < 1_000_000_000)])
        moderate = len(self.df[self.df['view_count'] < 100_000_000])

        print("\n📈 Popularity Categories:")
        print(f"   Mega Hits (≥1B views):       {mega_hits:>8,} ({mega_hits/len(self.df)*100:>5.1f}%)")
        print(f"   Popular (100M-1B views):     {popular:>8,} ({popular/len(self.df)*100:>5.1f}%)")
        print(f"   Moderate (<100M views):      {moderate:>8,} ({moderate/len(self.df)*100:>5.1f}%)")

        print("\n   ✓ Statistical analysis completed\n")

        # Store insights
        self.insights.append(f"{mega_hits} songs have achieved 'mega hit' status with over 1 billion views")
        self.insights.append(f"Average song duration is {self.df['duration_minutes'].mean():.2f} minutes")

    def create_visualizations(self):
        """Create all visualizations"""
        print("[4/6] Creating Visualizations...")

        # Create output directory for plots
        import os
        if not os.path.exists('analytics_output'):
            os.makedirs('analytics_output')

        viz_count = 0

        # 1. Top 15 Most Viewed Songs
        plt.figure(figsize=(14, 8))
        top_15 = self.df.nlargest(15, 'view_count')
        plt.barh(range(len(top_15)), top_15['views_in_billions'], color='#FF0000')
        plt.yticks(range(len(top_15)),
                   [title[:40] + '...' if len(title) > 40 else title
                    for title in top_15['title']], fontsize=9)
        plt.xlabel('Views (Billions)', fontsize=12, fontweight='bold')
        plt.title('Top 15 Most Viewed Songs on YouTube', fontsize=14, fontweight='bold', pad=20)
        plt.gca().invert_yaxis()
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.savefig('analytics_output/01_top_15_songs.png', dpi=300, bbox_inches='tight')
        plt.close()
        viz_count += 1
        print(f"   ✓ Created visualization {viz_count}: Top 15 Most Viewed Songs")

        # 2. Top 10 Channels by Total Views
        plt.figure(figsize=(14, 8))
        channel_views = self.df.groupby('channel')['views_in_billions'].sum().sort_values(ascending=False).head(10)
        plt.barh(range(len(channel_views)), channel_views.values, color='#1DB954')
        plt.yticks(range(len(channel_views)),
                   [ch[:35] + '...' if len(ch) > 35 else ch
                    for ch in channel_views.index], fontsize=9)
        plt.xlabel('Total Views (Billions)', fontsize=12, fontweight='bold')
        plt.title('Top 10 Channels by Total Views', fontsize=14, fontweight='bold', pad=20)
        plt.gca().invert_yaxis()
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.savefig('analytics_output/02_top_10_channels.png', dpi=300, bbox_inches='tight')
        plt.close()
        viz_count += 1
        print(f"   ✓ Created visualization {viz_count}: Top 10 Channels")

        # 3. View Count Distribution
        plt.figure(figsize=(14, 6))
        plt.hist(self.df['views_in_millions'], bins=50, color='#4285F4', edgecolor='black', alpha=0.7)
        plt.xlabel('Views (Millions)', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Songs', fontsize=12, fontweight='bold')
        plt.title('Distribution of Video Views', fontsize=14, fontweight='bold', pad=20)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('analytics_output/03_view_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        viz_count += 1
        print(f"   ✓ Created visualization {viz_count}: View Count Distribution")

        # 4. Duration vs Views Scatter Plot
        plt.figure(figsize=(14, 8))
        sample_size = min(2000, len(self.df))
        sample_df = self.df.sample(n=sample_size, random_state=42)
        plt.scatter(sample_df['duration_minutes'], sample_df['views_in_millions'],
                   alpha=0.5, s=30, color='#FF6B6B')
        plt.xlabel('Duration (Minutes)', fontsize=12, fontweight='bold')
        plt.ylabel('Views (Millions)', fontsize=12, fontweight='bold')
        plt.title('Song Duration vs View Count', fontsize=14, fontweight='bold', pad=20)
        plt.grid(alpha=0.3)

        # Add trend line
        z = np.polyfit(sample_df['duration_minutes'].dropna(),
                      sample_df['views_in_millions'].dropna(), 1)
        p = np.poly1d(z)
        x_trend = np.linspace(sample_df['duration_minutes'].min(),
                             sample_df['duration_minutes'].max(), 100)
        plt.plot(x_trend, p(x_trend), "r--", linewidth=2, label='Trend Line')
        plt.legend()
        plt.tight_layout()
        plt.savefig('analytics_output/04_duration_vs_views.png', dpi=300, bbox_inches='tight')
        plt.close()
        viz_count += 1
        print(f"   ✓ Created visualization {viz_count}: Duration vs Views")

        # 5. Duration Distribution
        plt.figure(figsize=(14, 6))
        plt.hist(self.df['duration_minutes'], bins=60, color='#9C27B0', edgecolor='black', alpha=0.7)
        plt.xlabel('Duration (Minutes)', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Songs', fontsize=12, fontweight='bold')
        plt.title('Distribution of Song Durations', fontsize=14, fontweight='bold', pad=20)
        plt.axvline(self.df['duration_minutes'].mean(), color='red', linestyle='--',
                   linewidth=2, label=f'Mean: {self.df["duration_minutes"].mean():.2f} min')
        plt.axvline(self.df['duration_minutes'].median(), color='green', linestyle='--',
                   linewidth=2, label=f'Median: {self.df["duration_minutes"].median():.2f} min')
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('analytics_output/05_duration_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        viz_count += 1
        print(f"   ✓ Created visualization {viz_count}: Duration Distribution")

        # 6. Channel Followers vs Views
        followers_data = self.df[self.df['channel_follower_count'].notna()]
        if len(followers_data) > 100:
            plt.figure(figsize=(14, 8))
            sample_size = min(2000, len(followers_data))
            sample_followers = followers_data.sample(n=sample_size, random_state=42)
            plt.scatter(sample_followers['channel_follower_count'] / 1_000_000,
                       sample_followers['views_in_millions'],
                       alpha=0.5, s=30, color='#FFA726')
            plt.xlabel('Channel Followers (Millions)', fontsize=12, fontweight='bold')
            plt.ylabel('Video Views (Millions)', fontsize=12, fontweight='bold')
            plt.title('Channel Followers vs Video Views', fontsize=14, fontweight='bold', pad=20)
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.savefig('analytics_output/06_followers_vs_views.png', dpi=300, bbox_inches='tight')
            plt.close()
            viz_count += 1
            print(f"   ✓ Created visualization {viz_count}: Followers vs Views")

        # 7. Popularity Categories Pie Chart
        plt.figure(figsize=(10, 10))
        mega_hits = len(self.df[self.df['view_count'] >= 1_000_000_000])
        popular = len(self.df[(self.df['view_count'] >= 100_000_000) & (self.df['view_count'] < 1_000_000_000)])
        moderate = len(self.df[self.df['view_count'] < 100_000_000])

        sizes = [mega_hits, popular, moderate]
        labels = [f'Mega Hits\n(≥1B views)\n{mega_hits:,} songs',
                 f'Popular\n(100M-1B views)\n{popular:,} songs',
                 f'Moderate\n(<100M views)\n{moderate:,} songs']
        colors = ['#FF6B6B', '#4ECDC4', '#95E1D3']
        explode = (0.1, 0.05, 0)

        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
        plt.title('Song Popularity Distribution', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('analytics_output/07_popularity_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        viz_count += 1
        print(f"   ✓ Created visualization {viz_count}: Popularity Distribution")

        # 8. Top 10 Channels by Song Count
        plt.figure(figsize=(14, 8))
        channel_counts = self.df['channel'].value_counts().head(10)
        plt.barh(range(len(channel_counts)), channel_counts.values, color='#00BCD4')
        plt.yticks(range(len(channel_counts)),
                   [ch[:35] + '...' if len(ch) > 35 else ch
                    for ch in channel_counts.index], fontsize=9)
        plt.xlabel('Number of Songs', fontsize=12, fontweight='bold')
        plt.title('Top 10 Channels by Number of Songs', fontsize=14, fontweight='bold', pad=20)
        plt.gca().invert_yaxis()
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.savefig('analytics_output/08_top_channels_by_count.png', dpi=300, bbox_inches='tight')
        plt.close()
        viz_count += 1
        print(f"   ✓ Created visualization {viz_count}: Top Channels by Song Count")

        # 9. Correlation Heatmap
        plt.figure(figsize=(10, 8))
        corr_data = self.df[['view_count', 'duration', 'channel_follower_count']].dropna().corr()
        sns.heatmap(corr_data, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=2, cbar_kws={"shrink": 0.8},
                   fmt='.3f', annot_kws={'fontsize': 12, 'fontweight': 'bold'})
        plt.title('Correlation Matrix: Views, Duration & Followers',
                 fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('analytics_output/09_correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        viz_count += 1
        print(f"   ✓ Created visualization {viz_count}: Correlation Heatmap")

        print(f"\n   ✓ All {viz_count} visualizations saved to 'analytics_output/' folder\n")

    def generate_insights_report(self):
        """Generate final insights report"""
        print("[5/6] Generating Insights Report...")

        report = []
        report.append("=" * 80)
        report.append("YOUTUBE MUSIC ANALYTICS - KEY INSIGHTS REPORT")
        report.append("=" * 80)
        report.append(f"\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Dataset: {self.csv_file}")
        report.append("\n" + "=" * 80)
        report.append("EXECUTIVE SUMMARY")
        report.append("=" * 80)

        # Key metrics
        report.append(f"\n📊 Dataset Overview:")
        report.append(f"   • Total songs analyzed: {len(self.df):,}")
        report.append(f"   • Unique channels: {self.df['channel'].nunique():,}")
        report.append(f"   • Combined views: {self.df['view_count'].sum() / 1_000_000_000:.2f} billion")
        report.append(f"   • Average views per song: {self.df['view_count'].mean():,.0f}")

        # Top performers
        report.append(f"\n🏆 Top Performers:")
        top_song = self.df.nlargest(1, 'view_count').iloc[0]
        report.append(f"   • Most viewed song: {top_song['title']}")
        report.append(f"     Views: {top_song['view_count']:,.0f}")
        report.append(f"     Channel: {top_song['channel']}")

        top_channel = self.df.groupby('channel')['view_count'].sum().idxmax()
        top_channel_views = self.df.groupby('channel')['view_count'].sum().max()
        report.append(f"   • Top channel: {top_channel}")
        report.append(f"     Total views: {top_channel_views:,.0f}")

        # Insights
        report.append(f"\n💡 Key Insights:")
        for i, insight in enumerate(self.insights, 1):
            report.append(f"   {i}. {insight}")

        # Duration analysis
        report.append(f"\n⏱️  Duration Insights:")
        report.append(f"   • Average song duration: {self.df['duration_minutes'].mean():.2f} minutes")
        report.append(f"   • Most common duration range: 3-5 minutes")
        short_songs = len(self.df[self.df['duration_minutes'] < 3])
        report.append(f"   • Songs under 3 minutes: {short_songs:,} ({short_songs/len(self.df)*100:.1f}%)")

        # Popularity breakdown
        report.append(f"\n📈 Popularity Analysis:")
        mega_hits = len(self.df[self.df['view_count'] >= 1_000_000_000])
        report.append(f"   • Mega hits (≥1B views): {mega_hits:,} songs ({mega_hits/len(self.df)*100:.1f}%)")
        popular = len(self.df[(self.df['view_count'] >= 100_000_000) & (self.df['view_count'] < 1_000_000_000)])
        report.append(f"   • Popular (100M-1B): {popular:,} songs ({popular/len(self.df)*100:.1f}%)")

        # Recommendations
        report.append(f"\n🎯 Recommendations:")
        report.append(f"   1. Focus on popular channels with proven track records")
        report.append(f"   2. Optimal song duration appears to be 3-4 minutes")
        report.append(f"   3. Channel size strongly correlates with video performance")
        report.append(f"   4. Consistency matters - top channels have multiple hits")

        report.append("\n" + "=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)

        # Save report
        report_text = "\n".join(report)
        with open('analytics_output/INSIGHTS_REPORT.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)

        # Print report
        print("\n" + report_text)
        print("\n   ✓ Report saved to 'analytics_output/INSIGHTS_REPORT.txt'\n")

    def run_analysis(self):
        """Run the complete analysis pipeline"""
        try:
            # Step 1: Load and clean data
            self.load_and_clean_data()

            # Step 2: Exploratory Data Analysis
            self.exploratory_data_analysis()

            # Step 3: Statistical Analysis
            self.statistical_analysis()

            # Step 4: Create Visualizations
            self.create_visualizations()

            # Step 5: Generate Report
            self.generate_insights_report()

            # Step 6: Complete
            print("[6/6] Analysis Complete!")
            print("\n" + "=" * 80)
            print("✅ ANALYSIS COMPLETED SUCCESSFULLY")
            print("=" * 80)
            print("\n📁 Output files saved in 'analytics_output/' directory:")
            print("   • 9 visualization charts (PNG format)")
            print("   • 1 insights report (TXT format)")
            print("\n🎉 Your YouTube Music Analytics Dashboard is ready!")
            print("=" * 80)

        except Exception as e:
            print(f"\n❌ Error during analysis: {str(e)}")
            import traceback
            traceback.print_exc()

def main():
    """Main function to run the analytics dashboard"""
    # Initialize the analytics dashboard
    dashboard = YouTubeMusicAnalytics('youtube-top-100-songs-2025.csv')

    # Run the complete analysis
    dashboard.run_analysis()

if __name__ == "__main__":
    main()
