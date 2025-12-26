import argparse
import json
import random
from datetime import datetime, timedelta
from scrambler import random_state_scramble

def generate_scrambles_for_year(year: int, output_file: str, limit_days: int = None):
    # Initialize dictionary to store scrambles
    scrambles = {}
    
    # We want to cover every hour of the year
    start_time = datetime(year, 1, 1, 0, 0, 0)
    
    current_time = start_time
    
    # Pre-instantiate RNG. 
    # We use the standard random module which random_state_scramble uses by default if we don't pass one, 
    # but passing one allows for future seeding if needed.
    rng = random.Random()

    print(f"Generating scrambles for year {year}...")
    
    days_processed = 0
    last_processed_date = None

    while current_time.year == year:
        # Check limit
        if limit_days is not None and days_processed >= limit_days:
            break

        # Generate keys for this specific timestamp
        
        # Year key: y-YYYY
        y_key = f"y-{year}"
        if y_key not in scrambles:
            _, _, s = random_state_scramble(rng)
            scrambles[y_key] = s
            
        # Month key: m-YYYY-MM
        m_key = f"m-{year}-{current_time.month:02d}"
        if m_key not in scrambles:
            _, _, s = random_state_scramble(rng)
            scrambles[m_key] = s
            
        # Week key: w-YYYY-WW (ISO week)
        iso_year, iso_week, _ = current_time.isocalendar()
        w_key = f"w-{iso_year}-{iso_week:02d}"
        if w_key not in scrambles:
            _, _, s = random_state_scramble(rng)
            scrambles[w_key] = s
            
        # Day key: d-YYYY-MM-DD
        d_key = f"d-{year}-{current_time.month:02d}-{current_time.day:02d}"
        if d_key not in scrambles:
            _, _, s = random_state_scramble(rng)
            scrambles[d_key] = s
            
        # Hour key: h-YYYY-MM-DD-HH
        h_key = f"h-{year}-{current_time.month:02d}-{current_time.day:02d}-{current_time.hour:02d}"
        if h_key not in scrambles:
            _, _, s = random_state_scramble(rng)
            scrambles[h_key] = s
        
        # Progress tracking
        if current_time.date() != last_processed_date:
            if last_processed_date is not None:
                days_processed += 1
            last_processed_date = current_time.date()
            if current_time.hour == 0:
                 print(f"Processing {current_time.date()}...", end='\r')

        # Increment by 1 hour
        current_time += timedelta(hours=1)

    # Sort dictionary by key for cleaner JSON (optional but nice)
    # But standard dicts preserve insertion order in modern Python. 
    # Sorting might mix types (y, m, w, d, h). 
    # Let's keep insertion order or just sort alphabetically. Alphabetical: d-, h-, m-, w-, y-
    # The user example had y, m, w, d, h hierarchy. Sorting alphabetically won't yield that.
    # Logic of loop adds y-Year first, then m-Jan, w-Week1, d-01, h-00, h-01...
    # Insertion order is naturally somewhat hierarchical.
    
    print(f"Generated {len(scrambles)} scrambles.")
    print(f"Writing to {output_file}...")
    
    with open(output_file, 'w') as f:
        json.dump(scrambles, f, indent=2)
        
    print("Done.")

def main():
    parser = argparse.ArgumentParser(description="Generate 3x3 scrambles for a full year.")
    parser.add_argument("--year", type=int, required=True, help="The year to generate scrambles for (e.g. 2025)")
    parser.add_argument("--limit-days", type=int, default=None, help="Limit the number of days to generate for testing")
    
    args = parser.parse_args()
    
    output_filename = f"scrambles-{args.year}.json"
    generate_scrambles_for_year(args.year, output_filename, args.limit_days)

if __name__ == "__main__":
    main()
