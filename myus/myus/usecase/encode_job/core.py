from myus.domain.encode_job.interface import EncodeJobInterface, FilterOption, PageOption, SortOption
from myus.injectors.container import injector
from myus.utils.common.result import FatalError, Result
from ._convert import ENCODE_JOB_MAX_ATTEMPTS, save_failed_encode_job_data, save_processed_encode_job_data


@Result.shield_exception()
def process_encode_jobs(limit: int) -> Result[int, FatalError]:
    repo = injector.get(EncodeJobInterface)
    ids_ret = repo.get_ids(FilterOption(is_processed=False, max_attempts=ENCODE_JOB_MAX_ATTEMPTS), SortOption(), PageOption(limit=limit))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    jobs_ret = repo.bulk_get(ids_ret.ok_value)
    if jobs_ret.is_err:
        return Result.err(jobs_ret.err_value)

    jobs = jobs_ret.ok_value
    processed_count = 0
    for job in jobs:
        process_ret = save_processed_encode_job_data(job)
        if process_ret.is_ok:
            processed_count += 1
            continue

        failed_ret = save_failed_encode_job_data(job, process_ret.err_value.message)
        if failed_ret.is_err:
            return Result.err(failed_ret.err_value)

    return Result.ok(processed_count)
