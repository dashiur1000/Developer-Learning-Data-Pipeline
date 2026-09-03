def process_record(raw_record: dict) -> dict:
    processed = raw_record.copy()
    years_code = processed.get('YearsCode')
    try:
        if years_code is not None and str(years_code).strip() != '':
            processed['YearsCode'] = int(float(years_code))
        else:
            processed['YearsCode'] = None
    except (ValueError, TypeError):
        processed['YearsCode'] = None

    learn_code_raw = processed.get('LearnCode', '')
    if learn_code_raw:
        processed['LearnCode'] = [item.strip() for item in learn_code_raw.split(';') if item.strip()]
    else:
        processed['LearnCode'] = []

    yc = processed['YearsCode']
    if yc is None:
        processed['experienceLevel'] = 'Unknown'
    elif 0 <= yc <= 2:
        processed['experienceLevel'] = 'Beginner'
    elif 3 <= yc <= 5:
        processed['experienceLevel'] = 'Early Career'
    elif 6 <= yc <= 10:
        processed['experienceLevel'] = 'Experienced'
    else:
        processed['experienceLevel'] = 'Highly Experienced'

    learn_list = processed['LearnCode']
    processed['usesDocumentation'] = any('documentation' in item.lower() for item in learn_list)
    processed['usesAIForLearning'] = any('ai' in item.lower() or 'code gen' in item.lower() for item in learn_list)
    processed['usesStackOverflow'] = any('stack overflow' in item.lower() for item in learn_list)

    return processed
