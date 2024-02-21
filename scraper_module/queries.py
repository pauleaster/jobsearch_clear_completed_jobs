
class SQLQueries:
    
    SET_EXPIRED_JOB = """
                UPDATE jobs
                SET comments = 'This job is no longer advertised'
                WHERE job_number = ?;
                """

    GET_NULL_COMMENT_JOBS = """
                SELECT j.job_number, j.comments
                FROM jobs j
                WHERE j.job_id IN (
                    SELECT DISTINCT job_id
                    FROM job_search_terms
                    WHERE valid = 1
                )
                and (j.comments is NULL)
                order by j.job_number;
                """
