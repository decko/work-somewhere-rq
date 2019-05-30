web: gunicorn telephone.wsgi
worker: python -u ./manage.py rqworker default registry-service registry-service-done call-service-done bill-service-done

worker_default: python -u ./manage.py rqworker default
worker_registry_service: python -u ./manage.py rqworker default registry-service
worker_registry_service_done: python -u ./manage.py rqworker registry-service-done
worker_call_service_done: python -u ./manage.py rqworker call-service-done
worker_bill_service_done: python -u ./manage.py rqworker bill-service-done
