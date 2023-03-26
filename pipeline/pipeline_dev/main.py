import sys
import click
from datetime import datetime, timedelta, timezone
import settings
from pipeline import controller

# @click.option('--upload-only', is_flag=True, help='업로드만진행할경우')
# @click.option('-dm', '--custom-delete-month', type = click.STRING, default='', help='삭제작업연월')

@click.command()
@click.option('-m', '--custom-batch-month', type = click.STRING, default='', help='배치작업연월')
def start_batch(custom_batch_month):
    batch_month = _get_batch_month(custom_batch_month)
    print('start_batch > batch_month : ', batch_month)
    if not batch_month:
        sys.exit(1)
    try:
        print('start_contoller')
        controller.etl(batch_month)
    except Exception as e:
        print(e)
        sys.exit(1)
    sys.exit(0)

def _get_batch_month(custom_batch_month):
    if custom_batch_month:
        print('custom_batch > batch_month : ', custom_batch_month)
        return _check_valid_month(custom_batch_month)

    first_day = datetime.today().replace(day = 1)
    
    batch_month = first_day - timedelta(days = 1)
  
    return batch_month.strftime('%Y%m')

# def _get_delete_month(custom_batch_month):
#     if custom_batch_month:
#         return _check_valid_month(custom_batch_month)

#     first_day = datetime.today().replace(day = 1)
#     delete_month = first_day + relativedelta(months = -13)
#     return delete_month.strftime('%Y%m')

def _check_valid_month(str_yyyymm):
    try:
        print('check_valid:', str_yyyymm)
        datetime.strptime(str_yyyymm, '%Y%m')
        return str_yyyymm
    except Exception as e:
        return None   


if __name__ == '__main__':
    start_batch()