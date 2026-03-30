from pipeline import fetch_raw_data, validate_data, clean_data, transform_data
from healer import diagnose_and_fix
from database import init_db, log_run, save_clean_data, get_run_history

MAX_ATTEMPTS = 3

def run_pipeline():
    print("\n=== Self-Healing Data Pipeline Agent ===")
    init_db()
    applied_fixes = []

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n--- Attempt {attempt}/{MAX_ATTEMPTS} ---")

        # Step 1: Fetch data
        print("Fetching raw data...")
        df = fetch_raw_data()
        print(f"Fetched {len(df)} rows")

        # Step 2: Apply any previous fixes
        if applied_fixes:
            print(f"Applying {len(applied_fixes)} fixes from previous attempt...")
            df = clean_data(df, applied_fixes)

        # Step 3: Validate
        print("Validating data...")
        is_valid, errors = validate_data(df)

        if is_valid:
            # Step 4: Transform and save
            print("Validation passed! Transforming data...")
            df = transform_data(df)
            save_clean_data(df)
            log_run("SUCCESS", attempt, [], applied_fixes, len(df))
            print(f"Pipeline completed successfully on attempt {attempt}!")
            print(f"Saved {len(df)} clean rows to database.")
            break
        else:
            print(f"Validation failed with {len(errors)} errors:")
            for e in errors:
                print(f"  ERROR: {e}")

            if attempt < MAX_ATTEMPTS:
                print("\nAI diagnosing errors...")
                heal = diagnose_and_fix(errors, attempt)
                print(f"Diagnosis: {heal['diagnosis']}")
                print(f"Confidence: {heal['confidence']}")
                print("Fixes generated:")
                for fix in heal["fixes"]:
                    print(f"  FIX: {fix}")
                applied_fixes.extend(heal["fixes"])
                log_run("FAILED", attempt, errors, heal["fixes"], len(df))
                print("\nRetrying with fixes applied...")
            else:
                log_run("FAILED", attempt, errors, [], len(df))
                print("\nMax attempts reached. Manual intervention required.")

    print("\n--- Run History ---")
    print(get_run_history().to_string())

if __name__ == "__main__":
    run_pipeline()