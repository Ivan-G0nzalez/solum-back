from fastapi import APIRouter, HTTPException, Depends
import pandas as pd
import os
from app.utils.logger import logger
from app.repositories.unit_of_work import UnitOfWork
from app.domain.call_models import AgentEnvironment, CallType
from app.domain.evaluation_models import EvaluatorType

router = APIRouter(prefix="/test", tags=["test"])

def parse_datetime(value):
    try:
        if pd.isna(value) or value == 'NaT' or value == '' or value is None:
            return None
        parsed = pd.to_datetime(value, errors='coerce')
        if pd.isna(parsed):
            return None
        return parsed
    except:
        return None

def parse_float(value):
    try:
        if pd.isna(value) or value == 'NaT' or value == '' or value is None:
            return None
        return float(str(value).replace(",", "."))
    except:
        return None

COLUMN_MAP = {
    'call_id': ['call_id'],
    'type': ['type', 'call_type_value'],
    'assistant': ['assistant'],
    'customer_phone': ['customer_phone_number', 'customer_phone'],
    'customer_name': ['customer_name'],
    'call_reason': ['call_reason'],
    'call_start_time': ['call_start_time'],
    'call_ended_time': ['call_ended_time'],
    'duration': ['duration'],
    'summary': ['summary'],
    'recording_url': ['recording_url'],
    'ended_reason': ['ended_reason'],
    'reviewer': ['Reviewer'],
    'evaluation': ['Evaluation', 'evaluation'],
    'check': ['QA Check', 'check'],
    'feedback': ['Feedback QA', 'feedback'],
    'score': ['Vapi QA Score', 'vapi_score'],
    'status_feedback_engineer': ['Status Feedback Engineer', 'status_feedback_engineer'],
    'comments_engineer': ['Comments Engineer', 'comments_engineer'],
}

def map_columns(df):
    if isinstance(df, pd.Series):
        df = df.to_frame().T
    new_df = pd.DataFrame()
    for standard_col, possible_cols in COLUMN_MAP.items():
        for col in possible_cols:
            if col in df.columns:
                new_df[standard_col] = df[col]
                break
        if standard_col not in new_df:
            new_df[standard_col] = None
    return new_df

@router.get("/read-excel", summary="Leer archivo Excel de prueba")
def read_excel_file():

    try:
        # Ruta absoluta al archivo en la raíz del proyecto
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../Technical Challenge Solum Health.xlsx")
        )
        xl = pd.read_excel(file_path, sheet_name=None, dtype=str)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error leyendo el archivo: {e}") 

    uow = UnitOfWork()
    
    try:
        for clinic_name, df in xl.items():
            if df.empty:
                continue
            
            # Map columns
            df = map_columns(df)

            clinic = uow.clinics.get_by_name(clinic_name.strip())
            if not clinic:
                clinic = uow.clinics.create({'name': clinic_name.strip()})

            for _, row in df.iterrows():
                if not row['call_id']:
                    continue

                # Get or create call
                existing_call = uow.calls.get_by_call_id(row['call_id'])
                if not existing_call:
                    try:
                        call_type = CallType[row['type']] if row['type'] in CallType.__members__ else CallType.inbound
                        new_call = {
                            'call_id': row['call_id'],
                            'call_type': call_type,
                            'agent_environment': AgentEnvironment.production,
                            'assistant': row['assistant'],
                            'customer_phone': row['customer_phone'],
                            'customer_name': row['customer_name'],
                            'call_reason': row['call_reason'],
                            'call_start_time': parse_datetime(row['call_start_time']),
                            'call_ended_time': parse_datetime(row['call_ended_time']),
                            'duration': parse_float(row['duration']),
                            'summary': row['summary'],
                            'recording_url': row['recording_url'],
                            'ended_reason': row['ended_reason'],
                            'clinic_id': clinic.id,
                        }
                        call = uow.calls.create(new_call)
                    except Exception as e:
                        logger.error(f"Error creating call {row['call_id']}: {e}")
                        continue
                
                else:
                    call = existing_call

                if row['evaluation'] or row['reviewer'] or row['feedback']:
                    try:
                        evaluation_data = {
                            'call_id': call.id,
                            'evaluator_type': EvaluatorType.LLM,
                            'reviewer': row['reviewer'],
                            'evaluation': row['evaluation'],
                            'check': row['check'],
                            'feedback': row['feedback'],
                            'score': parse_float(row['score']),
                            'status_feedback_engineer': row['status_feedback_engineer'],
                            'comments_engineer': row['comments_engineer']
                        }
                        uow.evaluations.create(evaluation_data)
                    except Exception as e:
                        logger.error(f"Error adding evaluation to call {row['call_id']}: {e}")
                        continue

        uow._UnitOfWork__session.commit()
        return {"detail": "Calls uploaded and processed successfully"}
        
    except Exception as e:
        uow._UnitOfWork__session.rollback()
        logger.error(f"Error processing Excel file: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing Excel file: {e}")