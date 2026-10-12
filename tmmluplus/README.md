---
license: mit
license_name: mit
task_categories:
- question-answering
language:
- zh
tags:
- traditional chinese
- finance
- medical
- taiwan
- benchmark
- zh-tw
- zh-hant
pretty_name: tmmlu++
size_categories:
- 100K<n<1M
configs:
  - config_name: engineering_math
    data_files:
    - split: train
      path: "data/engineering_math_dev.csv"
    - split: validation
      path: "data/engineering_math_val.csv"
    - split: test
      path: "data/engineering_math_test.csv"
  - config_name: dentistry
    data_files:
    - split: train
      path: "data/dentistry_dev.csv"
    - split: validation
      path: "data/dentistry_val.csv"
    - split: test
      path: "data/dentistry_test.csv"
  - config_name: traditional_chinese_medicine_clinical_medicine
    data_files:
    - split: train
      path: "data/traditional_chinese_medicine_clinical_medicine_dev.csv"
    - split: validation
      path: "data/traditional_chinese_medicine_clinical_medicine_val.csv"
    - split: test
      path: "data/traditional_chinese_medicine_clinical_medicine_test.csv"
  - config_name: clinical_psychology
    data_files:
    - split: train
      path: "data/clinical_psychology_dev.csv"
    - split: validation
      path: "data/clinical_psychology_val.csv"
    - split: test
      path: "data/clinical_psychology_test.csv"
  - config_name: technical
    data_files:
    - split: train
      path: "data/technical_dev.csv"
    - split: validation
      path: "data/technical_val.csv"
    - split: test
      path: "data/technical_test.csv"
  - config_name: culinary_skills
    data_files:
    - split: train
      path: "data/culinary_skills_dev.csv"
    - split: validation
      path: "data/culinary_skills_val.csv"
    - split: test
      path: "data/culinary_skills_test.csv"
  - config_name: mechanical
    data_files:
    - split: train
      path: "data/mechanical_dev.csv"
    - split: validation
      path: "data/mechanical_val.csv"
    - split: test
      path: "data/mechanical_test.csv"
  - config_name: logic_reasoning
    data_files:
    - split: train
      path: "data/logic_reasoning_dev.csv"
    - split: validation
      path: "data/logic_reasoning_val.csv"
    - split: test
      path: "data/logic_reasoning_test.csv"
  - config_name: real_estate
    data_files:
    - split: train
      path: "data/real_estate_dev.csv"
    - split: validation
      path: "data/real_estate_val.csv"
    - split: test
      path: "data/real_estate_test.csv"
  - config_name: general_principles_of_law
    data_files:
    - split: train
      path: "data/general_principles_of_law_dev.csv"
    - split: validation
      path: "data/general_principles_of_law_val.csv"
    - split: test
      path: "data/general_principles_of_law_test.csv"
  - config_name: finance_banking
    data_files:
    - split: train
      path: "data/finance_banking_dev.csv"
    - split: validation
      path: "data/finance_banking_val.csv"
    - split: test
      path: "data/finance_banking_test.csv"
  - config_name: anti_money_laundering
    data_files:
    - split: train
      path: "data/anti_money_laundering_dev.csv"
    - split: validation
      path: "data/anti_money_laundering_val.csv"
    - split: test
      path: "data/anti_money_laundering_test.csv"
  - config_name: ttqav2
    data_files:
    - split: train
      path: "data/ttqav2_dev.csv"
    - split: validation
      path: "data/ttqav2_val.csv"
    - split: test
      path: "data/ttqav2_test.csv"
  - config_name: marketing_management
    data_files:
    - split: train
      path: "data/marketing_management_dev.csv"
    - split: validation
      path: "data/marketing_management_val.csv"
    - split: test
      path: "data/marketing_management_test.csv"
  - config_name: business_management
    data_files:
    - split: train
      path: "data/business_management_dev.csv"
    - split: validation
      path: "data/business_management_val.csv"
    - split: test
      path: "data/business_management_test.csv"
  - config_name: organic_chemistry
    data_files:
    - split: train
      path: "data/organic_chemistry_dev.csv"
    - split: validation
      path: "data/organic_chemistry_val.csv"
    - split: test
      path: "data/organic_chemistry_test.csv"
  - config_name: advance_chemistry
    data_files:
    - split: train
      path: "data/advance_chemistry_dev.csv"
    - split: validation
      path: "data/advance_chemistry_val.csv"
    - split: test
      path: "data/advance_chemistry_test.csv"
  - config_name: physics
    data_files:
    - split: train
      path: "data/physics_dev.csv"
    - split: validation
      path: "data/physics_val.csv"
    - split: test
      path: "data/physics_test.csv"
  - config_name: secondary_physics
    data_files:
    - split: train
      path: "data/secondary_physics_dev.csv"
    - split: validation
      path: "data/secondary_physics_val.csv"
    - split: test
      path: "data/secondary_physics_test.csv"
  - config_name: human_behavior
    data_files:
    - split: train
      path: "data/human_behavior_dev.csv"
    - split: validation
      path: "data/human_behavior_val.csv"
    - split: test
      path: "data/human_behavior_test.csv"
  - config_name: national_protection
    data_files:
    - split: train
      path: "data/national_protection_dev.csv"
    - split: validation
      path: "data/national_protection_val.csv"
    - split: test
      path: "data/national_protection_test.csv"
  - config_name: jce_humanities
    data_files:
    - split: train
      path: "data/jce_humanities_dev.csv"
    - split: validation
      path: "data/jce_humanities_val.csv"
    - split: test
      path: "data/jce_humanities_test.csv"
  - config_name: politic_science
    data_files:
    - split: train
      path: "data/politic_science_dev.csv"
    - split: validation
      path: "data/politic_science_val.csv"
    - split: test
      path: "data/politic_science_test.csv"
  - config_name: agriculture
    data_files:
    - split: train
      path: "data/agriculture_dev.csv"
    - split: validation
      path: "data/agriculture_val.csv"
    - split: test
      path: "data/agriculture_test.csv"
  - config_name: official_document_management
    data_files:
    - split: train
      path: "data/official_document_management_dev.csv"
    - split: validation
      path: "data/official_document_management_val.csv"
    - split: test
      path: "data/official_document_management_test.csv"
  - config_name: financial_analysis
    data_files:
    - split: train
      path: "data/financial_analysis_dev.csv"
    - split: validation
      path: "data/financial_analysis_val.csv"
    - split: test
      path: "data/financial_analysis_test.csv"
  - config_name: pharmacy
    data_files:
    - split: train
      path: "data/pharmacy_dev.csv"
    - split: validation
      path: "data/pharmacy_val.csv"
    - split: test
      path: "data/pharmacy_test.csv"
  - config_name: educational_psychology
    data_files:
    - split: train
      path: "data/educational_psychology_dev.csv"
    - split: validation
      path: "data/educational_psychology_val.csv"
    - split: test
      path: "data/educational_psychology_test.csv"
  - config_name: statistics_and_machine_learning
    data_files:
    - split: train
      path: "data/statistics_and_machine_learning_dev.csv"
    - split: validation
      path: "data/statistics_and_machine_learning_val.csv"
    - split: test
      path: "data/statistics_and_machine_learning_test.csv"
  - config_name: management_accounting
    data_files:
    - split: train
      path: "data/management_accounting_dev.csv"
    - split: validation
      path: "data/management_accounting_val.csv"
    - split: test
      path: "data/management_accounting_test.csv"
  - config_name: introduction_to_law
    data_files:
    - split: train
      path: "data/introduction_to_law_dev.csv"
    - split: validation
      path: "data/introduction_to_law_val.csv"
    - split: test
      path: "data/introduction_to_law_test.csv"
  - config_name: computer_science
    data_files:
    - split: train
      path: "data/computer_science_dev.csv"
    - split: validation
      path: "data/computer_science_val.csv"
    - split: test
      path: "data/computer_science_test.csv"
  - config_name: veterinary_pathology
    data_files:
    - split: train
      path: "data/veterinary_pathology_dev.csv"
    - split: validation
      path: "data/veterinary_pathology_val.csv"
    - split: test
      path: "data/veterinary_pathology_test.csv"
  - config_name: accounting
    data_files:
    - split: train
      path: "data/accounting_dev.csv"
    - split: validation
      path: "data/accounting_val.csv"
    - split: test
      path: "data/accounting_test.csv"
  - config_name: fire_science
    data_files:
    - split: train
      path: "data/fire_science_dev.csv"
    - split: validation
      path: "data/fire_science_val.csv"
    - split: test
      path: "data/fire_science_test.csv"
  - config_name: optometry
    data_files:
    - split: train
      path: "data/optometry_dev.csv"
    - split: validation
      path: "data/optometry_val.csv"
    - split: test
      path: "data/optometry_test.csv"
  - config_name: insurance_studies
    data_files:
    - split: train
      path: "data/insurance_studies_dev.csv"
    - split: validation
      path: "data/insurance_studies_val.csv"
    - split: test
      path: "data/insurance_studies_test.csv"
  - config_name: pharmacology
    data_files:
    - split: train
      path: "data/pharmacology_dev.csv"
    - split: validation
      path: "data/pharmacology_val.csv"
    - split: test
      path: "data/pharmacology_test.csv"
  - config_name: taxation
    data_files:
    - split: train
      path: "data/taxation_dev.csv"
    - split: validation
      path: "data/taxation_val.csv"
    - split: test
      path: "data/taxation_test.csv"
  - config_name: trust_practice
    data_files:
    - split: train
      path: "data/trust_practice_dev.csv"
    - split: validation
      path: "data/trust_practice_val.csv"
    - split: test
      path: "data/trust_practice_test.csv"
  - config_name: geography_of_taiwan
    data_files:
    - split: train
      path: "data/geography_of_taiwan_dev.csv"
    - split: validation
      path: "data/geography_of_taiwan_val.csv"
    - split: test
      path: "data/geography_of_taiwan_test.csv"
  - config_name: physical_education
    data_files:
    - split: train
      path: "data/physical_education_dev.csv"
    - split: validation
      path: "data/physical_education_val.csv"
    - split: test
      path: "data/physical_education_test.csv"
  - config_name: auditing
    data_files:
    - split: train
      path: "data/auditing_dev.csv"
    - split: validation
      path: "data/auditing_val.csv"
    - split: test
      path: "data/auditing_test.csv"
  - config_name: administrative_law
    data_files:
    - split: train
      path: "data/administrative_law_dev.csv"
    - split: validation
      path: "data/administrative_law_val.csv"
    - split: test
      path: "data/administrative_law_test.csv"
  - config_name: education_(profession_level)
    data_files:
    - split: train
      path: "data/education_(profession_level)_dev.csv"
    - split: validation
      path: "data/education_(profession_level)_val.csv"
    - split: test
      path: "data/education_(profession_level)_test.csv"
  - config_name: economics
    data_files:
    - split: train
      path: "data/economics_dev.csv"
    - split: validation
      path: "data/economics_val.csv"
    - split: test
      path: "data/economics_test.csv"
  - config_name: veterinary_pharmacology
    data_files:
    - split: train
      path: "data/veterinary_pharmacology_dev.csv"
    - split: validation
      path: "data/veterinary_pharmacology_val.csv"
    - split: test
      path: "data/veterinary_pharmacology_test.csv"
  - config_name: nautical_science
    data_files:
    - split: train
      path: "data/nautical_science_dev.csv"
    - split: validation
      path: "data/nautical_science_val.csv"
    - split: test
      path: "data/nautical_science_test.csv"
  - config_name: occupational_therapy_for_psychological_disorders
    data_files:
    - split: train
      path: "data/occupational_therapy_for_psychological_disorders_dev.csv"
    - split: validation
      path: "data/occupational_therapy_for_psychological_disorders_val.csv"
    - split: test
      path: "data/occupational_therapy_for_psychological_disorders_test.csv"
  - config_name: basic_medical_science
    data_files:
    - split: train
      path: "data/basic_medical_science_dev.csv"
    - split: validation
      path: "data/basic_medical_science_val.csv"
    - split: test
      path: "data/basic_medical_science_test.csv"
  - config_name: macroeconomics
    data_files:
    - split: train
      path: "data/macroeconomics_dev.csv"
    - split: validation
      path: "data/macroeconomics_val.csv"
    - split: test
      path: "data/macroeconomics_test.csv"
  - config_name: trade
    data_files:
    - split: train
      path: "data/trade_dev.csv"
    - split: validation
      path: "data/trade_val.csv"
    - split: test
      path: "data/trade_test.csv"
  - config_name: chinese_language_and_literature
    data_files:
    - split: train
      path: "data/chinese_language_and_literature_dev.csv"
    - split: validation
      path: "data/chinese_language_and_literature_val.csv"
    - split: test
      path: "data/chinese_language_and_literature_test.csv"
  - config_name: tve_design
    data_files:
    - split: train
      path: "data/tve_design_dev.csv"
    - split: validation
      path: "data/tve_design_val.csv"
    - split: test
      path: "data/tve_design_test.csv"
  - config_name: junior_science_exam
    data_files:
    - split: train
      path: "data/junior_science_exam_dev.csv"
    - split: validation
      path: "data/junior_science_exam_val.csv"
    - split: test
      path: "data/junior_science_exam_test.csv"
  - config_name: junior_math_exam
    data_files:
    - split: train
      path: "data/junior_math_exam_dev.csv"
    - split: validation
      path: "data/junior_math_exam_val.csv"
    - split: test
      path: "data/junior_math_exam_test.csv"
  - config_name: junior_chinese_exam
    data_files:
    - split: train
      path: "data/junior_chinese_exam_dev.csv"
    - split: validation
      path: "data/junior_chinese_exam_val.csv"
    - split: test
      path: "data/junior_chinese_exam_test.csv"
  - config_name: junior_social_studies
    data_files:
    - split: train
      path: "data/junior_social_studies_dev.csv"
    - split: validation
      path: "data/junior_social_studies_val.csv"
    - split: test
      path: "data/junior_social_studies_test.csv"
  - config_name: tve_mathematics
    data_files:
    - split: train
      path: "data/tve_mathematics_dev.csv"
    - split: validation
      path: "data/tve_mathematics_val.csv"
    - split: test
      path: "data/tve_mathematics_test.csv"
  - config_name: tve_chinese_language
    data_files:
    - split: train
      path: "data/tve_chinese_language_dev.csv"
    - split: validation
      path: "data/tve_chinese_language_val.csv"
    - split: test
      path: "data/tve_chinese_language_test.csv"
  - config_name: tve_natural_sciences
    data_files:
    - split: train
      path: "data/tve_natural_sciences_dev.csv"
    - split: validation
      path: "data/tve_natural_sciences_val.csv"
    - split: test
      path: "data/tve_natural_sciences_test.csv"
  - config_name: junior_chemistry
    data_files:
    - split: train
      path: "data/junior_chemistry_dev.csv"
    - split: validation
      path: "data/junior_chemistry_val.csv"
    - split: test
      path: "data/junior_chemistry_test.csv"
  - config_name: music
    data_files:
    - split: train
      path: "data/music_dev.csv"
    - split: validation
      path: "data/music_val.csv"
    - split: test
      path: "data/music_test.csv"
  - config_name: education
    data_files:
    - split: train
      path: "data/education_dev.csv"
    - split: validation
      path: "data/education_val.csv"
    - split: test
      path: "data/education_test.csv"
  - config_name: three_principles_of_people
    data_files:
    - split: train
      path: "data/three_principles_of_people_dev.csv"
    - split: validation
      path: "data/three_principles_of_people_val.csv"
    - split: test
      path: "data/three_principles_of_people_test.csv"
  - config_name: taiwanese_hokkien
    data_files:
    - split: train
      path: "data/taiwanese_hokkien_dev.csv"
    - split: validation
      path: "data/taiwanese_hokkien_val.csv"
    - split: test
      path: "data/taiwanese_hokkien_test.csv"
---
# TMMLU+ : Large scale traditional chinese massive multitask language understanding

<p align="center">
<img src="https://huggingface.co/datasets/ikala/tmmluplus/resolve/main/resources/cover.png" alt="A close-up image of a neat paper note with a white background. The text 'TMMLU+' is written horizontally across the center of the note in bold, black." style="max-width: 400" width=400 />
</p>

iKala presents **TMMLU+**, a large-scale benchmark for evaluating LLM capabilities in **Traditional Chinese, with content primarily reflecting Taiwan's linguistic, educational, and professional contexts**. It covers **66 subjects**, from elementary to professional domains, and is approximately **six times larger** than [TMMLU](https://github.com/mtkresearch/TCEval) with broader, more balanced coverage.

**TMMLU+ v1.1** improves benchmark quality through systematic review: outdated legal and regulatory content was updated, incomplete or invalid questions were corrected or removed, and ambiguous items were reviewed by domain experts. Questions without a single defensible answer were excluded.


```python
from datasets import load_dataset
task_list = [
             'engineering_math', 'dentistry', 'traditional_chinese_medicine_clinical_medicine', 'clinical_psychology', 'technical', 'culinary_skills', 'mechanical', 'logic_reasoning', 'real_estate',
             'general_principles_of_law', 'finance_banking', 'anti_money_laundering', 'ttqav2', 'marketing_management', 'business_management', 'organic_chemistry', 'advance_chemistry',
             'physics', 'secondary_physics', 'human_behavior', 'national_protection', 'jce_humanities', 'politic_science', 'agriculture', 'official_document_management',
             'financial_analysis', 'pharmacy', 'educational_psychology', 'statistics_and_machine_learning', 'management_accounting', 'introduction_to_law', 'computer_science', 'veterinary_pathology',
             'accounting', 'fire_science', 'optometry', 'insurance_studies', 'pharmacology', 'taxation', 'trust_practice', 'geography_of_taiwan', 'physical_education', 'auditing', 'administrative_law',
             'education_(profession_level)', 'economics', 'veterinary_pharmacology', 'nautical_science', 'occupational_therapy_for_psychological_disorders',
             'basic_medical_science', 'macroeconomics', 'trade', 'chinese_language_and_literature', 'tve_design', 'junior_science_exam', 'junior_math_exam', 'junior_chinese_exam',
             'junior_social_studies', 'tve_mathematics', 'tve_chinese_language', 'tve_natural_sciences', 'junior_chemistry', 'music', 'education', 'three_principles_of_people',
             'taiwanese_hokkien'
            ]
for task in task_list:
  val = load_dataset('ikala/tmmluplus', task)['validation']
  dev = load_dataset('ikala/tmmluplus', task)['train']
  test = load_dataset('ikala/tmmluplus', task)['test']
```

For each dataset split

```python
for row in test:
  print(row)
  break
>> Dataset({
    features: ['question', 'A', 'B', 'C', 'D', 'answer'],
    num_rows: 11
})
```

Statistic on all four categories : STEM, Social Science, Humanities, Other

| Category                         | Test  | Dev  | Validation |
|----------------------------------|-------|------|------------|
| STEM                             | 3458  | 70   | 385        |
| Social Sciences                  | 5958  | 90   | 665        |
| Humanities                       | 1763  | 35   | 197        |
| Other (Business, Health, Misc.)  | 8939  | 135  | 995        |
| **Total**                        | 20118 | 330  | 2242       |


## Dataset Versions

| Version | Tag | Description |
|---|---|---|
| v1.0 | [`v1.0`](https://huggingface.co/datasets/ikala/tmmluplus/tree/v1.0) | Original release, unmodified |
| v1.1 | [`v1.1`](https://huggingface.co/datasets/ikala/tmmluplus/tree/v1.1) | Verified and corrected release (see below) — **this page reflects v1.1** |

v1.1 was produced by individually re-verifying every question flagged as potentially problematic by four rule-based scans (6,116 candidate questions out of 22,742), followed by a human review pass on the 691 questions where the verification suggested a change.

- **197** questions had their answer corrected — 196 with the answer key changed (`change_answer`), plus 1 whose stem was rewritten to fix a corrupted/duplicated fragment (all 4 options and the answer were kept)
- **539** questions were removed entirely (255 `change_content` — defective stem/options; 233 `expert_review` — unresolved ambiguity even after review; 51 `remove` — flagged in an earlier review pass)
- **22,203** questions remain in v1.1 (out of 22,742 in v1.0)

| Category                         | Test  | Dev  | Validation |
|-----------------------------------|-------|------|------------|
| STEM                              | 3369  | 69   | 382        |
| Social Sciences                   | 5864  | 89   | 657        |
| Humanities                        | 1723  | 34   | 189        |
| Other (Business, Health, Misc.)   | 8724  | 129  | 974        |
| **Total**                         | **19680** | **321** | **2202** |

*(For v1.0 figures, see the "Statistic on all four categories" table above, or load `revision="v1.0"`.)*

To load a specific version:

```python
from datasets import load_dataset
load_dataset('ikala/tmmluplus', 'accounting', revision='v1.0')  # original
load_dataset('ikala/tmmluplus', 'accounting', revision='v1.1')  # verified/corrected
```


## Leaderboard

Scores below are computed against the v1.1 question set for the 21 models that have completed evaluation on all 66 subjects. Category and Total scores are the average of each category's own accuracy (STEM/Social Science/Humanities/Other weighted equally, matching the [`ievals`](https://github.com/iKala/ievals) methodology), not a per-question average. For v1.0 scores, load `revision="v1.0"` and re-run evaluation against that question set.

| Model | STEM | Social Science | Humanities | Other | Total |
|---|---|---|---|---|---|
| claude-opus-5 | **98.71** | **96.09** | **94.60** | **95.25** | **96.16** |
| gemini-3.7-flash (reasoning) | 93.37 | 92.09 | 88.91 | 87.64 | 90.50 |
| gpt-5.6-sol | 93.28 | 91.54 | 82.30 | 86.39 | 88.38 |
| claude-fable-5 | 90.61 | 83.41 | 90.02 | 84.22 | 87.06 |
| deepseek/deepseek-v4-pro-0813 | 92.89 | 89.24 | 79.63 | 83.92 | 86.42 |
| claude-sonnet-5 | 89.21 | 85.79 | 81.72 | 81.90 | 84.66 |
| gemini-3.1-pro-preview (reasoning) | 87.14 | 83.22 | 84.91 | 81.76 | 84.26 |
| deepseek/deepseek-v4-flash | 89.42 | 86.72 | 77.42 | 80.42 | 83.50 |
| tencent/hy3 | 89.81 | 88.25 | 74.75 | 80.50 | 83.33 |
| gpt-5.6-terra | 90.22 | 86.95 | 72.49 | 80.07 | 82.43 |
| moonshotai/kimi-k3 | 86.12 | 82.55 | 77.31 | 78.03 | 81.00 |
| qwen/qwen3.7-max | 85.07 | 84.02 | 76.03 | 77.25 | 80.59 |
| qwen/qwen3.8-27b | 93.10 | 83.99 | 63.49 | 79.61 | 80.05 |
| gpt-5.6-luna | 87.59 | 83.65 | 70.81 | 76.48 | 79.63 |
| z-ai/glm-5.2 | 85.31 | 83.34 | 70.28 | 75.42 | 78.59 |
| xiaomi/mimo-v2.5 | 87.44 | 83.53 | 67.32 | 74.19 | 78.12 |
| minimax/minimax-m3 | 86.21 | 79.57 | 65.76 | 73.91 | 76.36 |
| x-ai/grok-4.3 | 81.32 | 81.65 | 67.67 | 74.79 | 76.36 |
| claude-haiku-4-5 | 82.88 | 74.54 | 59.37 | 70.14 | 71.73 |
| google/gemma-4-31b-it | 81.26 | 73.29 | 58.15 | 66.66 | 69.84 |
| nvidia/nemotron-3-ultra-550b-a55b | 72.77 | 73.99 | 59.20 | 63.96 | 67.48 |

*Note: all models were called with default API parameters (no reasoning effort or thinking mode explicitly configured). Models marked (reasoning) reported a separate reasoning/thinking token count from the API under this default before producing their final answer; other models answered directly without an exposed reasoning trace.*


## Licensing Information

This dataset is released under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, copy, modify, and redistribute it, including for commercial purposes, provided the original copyright notice is retained.


## Citation

```
@article{ikala2023eval,
  title={An Improved Traditional Chinese Evaluation Suite for Foundation Model},
  author={Tam, Zhi-Rui and Pai, Ya-Ting and Lee, Yen-Wei and Cheng, Sega and Shuai, Hong-Han},
  journal={arXiv preprint arXiv:2403.01858},
  year={2023}
}
```


## Contact

For questions, bug reports, leaderboard submissions, or collaboration inquiries regarding TMMLU+, please contact us at **[tmmluplus@ikala.ai](mailto:tmmluplus@ikala.ai)**.


## About iKala

iKala helps enterprises make better, faster decisions by embedding AI and data at the core of their business. We support AI transformation by helping organizations move from data to decisions, delivering full AI solutions that combine their first-party data with iKala's intelligence built on billions of global social signals.

Headquartered in Taiwan with a global footprint, iKala serves over 1,000 enterprises and 50,000 brands across more than 190 countries, including Fortune 500 companies.

<p style="line-height: 2.1;">
<img src="https://huggingface.co/datasets/ikala/tmmluplus/resolve/main/resources/ikala_logo.png" alt="iKala logo" width="26" style="display: inline-block; vertical-align: middle; border-radius: 6px; margin: 0 10px 0 0;" /><b style="display: inline-block; vertical-align: middle; min-width: 84px;">iKala</b><span style="vertical-align: middle;">Official Website: <a href="https://ikala.ai">ikala.ai</a></span><br />
<img src="https://huggingface.co/datasets/ikala/tmmluplus/resolve/main/resources/kolr_logo.png" alt="Kolr logo" width="26" style="display: inline-block; vertical-align: middle; border-radius: 6px; margin: 0 10px 0 0;" /><b style="display: inline-block; vertical-align: middle; min-width: 84px;">Kolr</b><span style="vertical-align: middle;">Official Website: <a href="https://kolr.ai">kolr.ai</a></span><br />
<img src="https://huggingface.co/datasets/ikala/tmmluplus/resolve/main/resources/kuroma_logo.png" alt="Kuroma logo" width="26" style="display: inline-block; vertical-align: middle; border-radius: 6px; margin: 0 10px 0 0;" /><b style="display: inline-block; vertical-align: middle; min-width: 84px;">Kuroma</b><span style="vertical-align: middle;">Official Website: <a href="https://kuroma.ai">kuroma.ai</a></span>
</p>
