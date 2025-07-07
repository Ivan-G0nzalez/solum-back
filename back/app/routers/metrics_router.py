from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from app.repositories.unit_of_work import UnitOfWork
from app.data_acess.models import Call, Evaluation, Clinic
from app.domain.call_models import CallType
from app.utils.logger import logger

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/dashboard", summary="Obtener métricas generales del dashboard")
def get_dashboard_metrics(
    clinic_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Obtiene métricas generales del dashboard incluyendo:
    - Total de clínicas
    - Total de llamadas
    - Total de evaluaciones
    - Llamadas con feedback
    - Duración promedio
    - Distribución de tipos de llamadas
    - Puntaje promedio de evaluaciones
    """
    try:
        uow = UnitOfWork()
        session = uow._UnitOfWork__session
        
        # Construir filtros base
        filters = []
        if clinic_id:
            filters.append(Call.clinic_id == clinic_id)
        
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                filters.append(Call.call_start_time >= start_dt)
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de fecha inválido para start_date")
        
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                filters.append(Call.call_start_time <= end_dt)
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de fecha inválido para end_date")
        
        # 1. Total de clínicas
        total_clinics = session.query(Clinic).count()
        
        # 2. Query base para llamadas
        base_query = session.query(Call)
        if filters:
            base_query = base_query.filter(and_(*filters))
        
        # 3. Total de llamadas
        total_calls = base_query.count()
        
        # 4. Duración promedio
        avg_duration_result = base_query.with_entities(
            func.avg(Call.duration)
        ).scalar()
        average_duration_seconds = float(avg_duration_result) if avg_duration_result else 0
        
        # 5. Total de evaluaciones
        evaluation_query = session.query(Evaluation).join(Call)
        if filters:
            evaluation_query = evaluation_query.filter(and_(*filters))
        total_evaluations = evaluation_query.count()
        
        # 6. Llamadas con feedback
        calls_with_feedback_query = session.query(Call).join(Evaluation).filter(
            Evaluation.feedback.isnot(None) & (Evaluation.feedback != '')
        )
        if filters:
            calls_with_feedback_query = calls_with_feedback_query.filter(and_(*filters))
        calls_with_feedback = calls_with_feedback_query.distinct().count()
        
        # 7. Distribución de tipos de llamadas
        call_types_query = session.query(
            Call.call_type,
            func.count(Call.id).label('count')
        )
        if filters:
            call_types_query = call_types_query.filter(and_(*filters))
        
        call_types_results = call_types_query.group_by(Call.call_type).all()
        
        call_types_distribution = []
        for result in call_types_results:
            percentage = (result.count / total_calls * 100) if total_calls > 0 else 0
            call_types_distribution.append({
                "call_type": result.call_type.value,
                "count": result.count,
                "percentage": round(percentage, 2)
            })
        
        # 8. Puntaje promedio de evaluaciones
        avg_score_query = session.query(
            func.avg(Evaluation.score).label('avg_score'),
            func.count(Evaluation.id).label('total_evaluations_with_score')
        ).join(Call)
        if filters:
            avg_score_query = avg_score_query.filter(and_(*filters))
        
        score_result = avg_score_query.first()
        average_score = round(float(score_result.avg_score or 0), 2)
        total_evaluations_with_score = score_result.total_evaluations_with_score
        
        # 9. Llamadas por clínica (top 5)
        calls_by_clinic_query = session.query(
            Clinic.name,
            func.count(Call.id).label('call_count')
        ).join(Call)
        if filters:
            calls_by_clinic_query = calls_by_clinic_query.filter(and_(*filters))
        
        calls_by_clinic = calls_by_clinic_query.group_by(Clinic.name)\
            .order_by(func.count(Call.id).desc())\
            .limit(5).all()
        
        top_clinics = [
            {"clinic_name": result.name, "call_count": result.call_count}
            for result in calls_by_clinic
        ]
        
        return {
            "total_clinics": total_clinics,
            "total_calls": total_calls,
            "total_evaluations": total_evaluations,
            "calls_with_feedback": calls_with_feedback,
            "average_duration_seconds": round(average_duration_seconds, 2),
            "average_score": average_score,
            "total_evaluations_with_score": total_evaluations_with_score,
            "call_types_distribution": call_types_distribution,
            "top_clinics": top_clinics,
            "filters_applied": {
                "clinic_id": clinic_id,
                "start_date": start_date,
                "end_date": end_date
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting dashboard metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas: {e}")

