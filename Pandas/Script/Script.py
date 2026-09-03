import pandas as pd
import json
import os

def main():
    df = load_file()
    YearsCode_to_numeric(df)
    passthrough_and_cats = ['AISelect', 'AIAcc', 'AISent', 'DevType', 'LearnCodeChoose', 'LearnCodeAI', 'Age']
    for col in passthrough_and_cats:
        if col in df.columns:
            df[col] = df[col].apply(clean_text_field)

    for col in ['LearnCode', 'AILearnHow']:
        if col in df.columns:
            def process_multi_select(val):
                cleaned = clean_text_field(val)
                if cleaned is None:
                    return None
                if isinstance(cleaned, list):
                    return cleaned
                return [item.strip() for item in str(cleaned).split(';') if item.strip()]

            df[col] = df[col].apply(process_multi_select)
    write_json(df)
    df = load_json()
    TECH_DOC = "Technical documentation (is generated for/by the tool or system)"
    AI_CODEGEN = "AI CodeGen tools or AI-enabled apps"
    STACK_OVERFLOW = "Stack Overflow or Stack Exchange"
    has_option(["Books", "Stack Overflow"], "Stack Overflow")
    df = apply(df, TECH_DOC, AI_CODEGEN, STACK_OVERFLOW)
    df = rename_columns(df)
    export(df)



def load_file():
    df = pd.read_csv("developer_ai_learning_raw.csv")
    return df

def YearsCode_to_numeric(df):
    df['YearsCode'] = pd.to_numeric(df['YearsCode'], errors='coerce').astype('Int64')

def split_values(df):
    df['AILearnHow'] = df['AILearnHow'].apply(lambda x: x.split(";") if isinstance(x, str) else None)
    df['LearnCode'] = df['LearnCode'].apply(lambda x: x.split(";") if isinstance(x, str) else None)

def clean_text_field(val):
    if val is None:
        return None
    if isinstance(val, (list, tuple)):
        items = [str(x).strip() for x in val if x is not None and str(x).strip().lower() not in ["nan", ""]]
        return items if items else None

    try:
        if pd.isna(val):
            return None
    except (ValueError, TypeError):
        pass

    s = str(val).strip()
    if s.lower() in ["nan", ""]:
        return None
    return s

def clean_text_field(val):
    if val is None:
        return None
    if isinstance(val, (list, tuple)):
        items = [str(x).strip() for x in val if x is not None and str(x).strip().lower() not in ["nan", ""]]
        return items if items else None

    try:
        if pd.isna(val):
            return None
    except (ValueError, TypeError):
        pass

    s = str(val).strip()
    if s.lower() in ["nan", ""]:
        return None
    return s

def write_json(df):
    with open("your_cleaned.jsonl", "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            record = {
                "ResponseId": int(row["ResponseId"]),
                "Age": row["Age"],
                "YearsCode": int(row["YearsCode"]) if row["YearsCode"] is not None and pd.notna(
                    row["YearsCode"]) else None,
                "DevType": row["DevType"],
                "LearnCodeChoose": row["LearnCodeChoose"],
                "LearnCode": row["LearnCode"],
                "LearnCodeAI": row["LearnCodeAI"],
                "AILearnHow": row["AILearnHow"],
                "AISelect": row["AISelect"],
                "AIAcc": row["AIAcc"],
                "AISent": row["AISent"],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

def load_json():
    records = []
    with open("your_cleaned.jsonl", "r") as f:
        for line in f:
            records.append(json.loads(line))

    df = pd.DataFrame(records)
    return df

def experience_level(years_code):
    if pd.isna(years_code):
        return "Unknown"
    if years_code <= 2:
        return "Beginner"
    if years_code <= 5:
        return "Early Career"
    if years_code <= 10:
        return "Experienced"
    return "Highly Experienced"

def has_option(options, target):
    if options is None:
        return False
    return target in options

def apply(df, TECH_DOC, AI_CODEGEN, STACK_OVERFLOW):
    df['experienceLevel'] = df['YearsCode'].apply(experience_level)
    df['usesDocumentation'] = df['LearnCode'].apply(lambda x: has_option(x, TECH_DOC))
    df['usesAIForLearning'] = df['LearnCode'].apply(lambda x: has_option(x, AI_CODEGEN))
    df['usesStackOverflow'] = df['LearnCode'].apply(lambda x: has_option(x, STACK_OVERFLOW))
    return df

def rename_columns(df):
    df = df.rename(columns={
        'ResponseId': 'responseId',
        'Age': 'age',
        'YearsCode': 'yearsCode',
        'DevType': 'devType',
        'LearnCodeChoose': 'learnCodeChoose',
        'LearnCode': 'learningMethods',
        'LearnCodeAI': 'learnCodeAI',
        'AILearnHow': 'aiLearningMethods',
        'AISelect': 'aiUsage',
        'AIAcc': 'aiTrust',
        'AISent': 'aiSentiment',
    })
    return df

def export(df):
    with open("your_processed.jsonl", "w") as f:
        for _, row in df.iterrows():
            record = row.to_dict()

            for key, value in record.items():
                if not isinstance(value, list) and pd.isna(value):
                    record[key] = None

            f.write(json.dumps(record) + "\n")

if __name__ == "__main__":
    main()