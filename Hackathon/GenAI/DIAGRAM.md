```mermaid
flowchart TD
    HealthcareProfessional[Healthcare Professional] -->|accesses| MedicalRecordsDatabase[(Medical Records Database)]
    MedicalRecordsDatabase -->|provides| MedicalRecords[Medical Records, Language Proficiencies, Personality Profile]
    MedicalRecords -->|LLM 0: record summary + LLM 1: communication tips| HealthcareProfessional
    Patient[Patient] -->|provides| HealthComplaints[Health Complaints]
    Patient -->|provides| Feedback[Feedback]
    Patient -->|has| Profile[16 Personalities Profile & Language/Medical Proficiencies]
    Feedback -->|updates| Profile
    Profile -->|stored in| MedicalRecordsDatabase
    HealthcareProfessional -->|communicates with| Patient
    HealthComplaints -->|to| HealthcareProfessional
    HealthcareProfessional -->|performs| Diagnosis[Diagnosis]
    Diagnosis -->|communicated with help of LLM 2| Patient
    MedicalRecordsDatabase -->|provides| ProfessionalRecords[Medical Records, Diagnosis, Referral Questions/Tasks]
    ProfessionalRecords -->|to| ColleagueHealthcareProfessionals[Colleague Healthcare Professionals]
    ProfessionalRecords -->|communicated with help of LLM 3| ColleagueHealthcareProfessionals
```

## Notes

- **Healthcare Professional**: Accesses medical records, language proficiencies, and personality profiles from the Medical Records Database. Optionally uses LLM 0 to summarize medical records. Gets communication suggestions for the Patient using LLM 1. Performs diagnosis and communicates results with help of LLM 2. Can communicate the same diagnosis and medical records to another Healthcare Professional using LLM 3.
- **Patient**: Provides health complaints and feedback to the Healthcare Professional. Has a profile that includes a 16 personalities profile and language/medical proficiencies.
- **Medical Records Database**: Stores medical records, language proficiencies, personality profiles, and feedback. Provides communication hints and professional records.
- **LLM 0**: Summarizes medical records.
- **LLM 1**: Provides communication suggestions for the Patient based on their profile and language proficiencies.
- **LLM 2**: Helps the Healthcare Professional communicate diagnosis results to the Patient.
- **LLM 3**: Helps the Healthcare Professional communicate diagnosis and medical records to another Healthcare Professional.
- **Colleague Healthcare Professionals**: Receive professional records, diagnosis, and referral questions/tasks from the Healthcare Professional.
