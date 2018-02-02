import logging

from dataactcore.interfaces.db import GlobalDB
from dataactcore.logging import configure_logging
from dataactvalidator.health_check import create_app

logger = logging.getLogger(__name__)


def main():
    sess = GlobalDB.db().session

    logger.info("Starting county code fixes, creating zip_county temporary view")

    # zip_county view creation
    sess.execute(
        """CREATE MATERIALIZED VIEW zip_county AS (
            SELECT
                concat(zip5, zip_last4) AS combined_zip,
                concat(zip5, '-', zip_last4) AS dashed_zip,
                zip5,
                zip_last4,
                cc.county_number,
                county_name
            FROM zips
            JOIN county_code AS cc
                ON cc.state_code = zips.state_abbreviation
                AND cc.county_number = zips.county_number)"""
    )
    sess.commit()

    logger.info("Created zip_county temporary view, creating zip_county indexes")

    sess.execute("CREATE INDEX ix_zip5_zip_county ON zip_county (zip5)")
    sess.execute("CREATE INDEX ix_zip_last4_zip_county ON zip_county (zip_last4)")
    sess.execute("CREATE INDEX ix_combined_zip_zip_county ON zip_county (combined_zip)")
    sess.execute("CREATE INDEX ix_dashed_zip_zip_county ON zip_county (dashed_zip)")
    sess.commit()

    logger.info("Created zip_county indexes, creating single_county temporary view")

    # single_county view creation
    sess.execute(
        """CREATE MATERIALIZED VIEW single_county AS (
            SELECT zip5, county_number, county_name
            FROM (SELECT
                zip5,
                county_number,
                county_name,
                ROW_NUMBER() OVER (PARTITION BY
                    zip5) AS row
                FROM zip_county) AS tmp
                WHERE tmp.row = 1)"""
    )
    sess.commit()

    logger.info("Created single_county temporary view, creating single_county index")

    sess.execute("CREATE INDEX ix_zip5_single_county ON single_county (zip5)")
    sess.commit()

    logger.info("Created single_county index, starting FPDS legal entity 9-digit zips without dashes")

    # FPDS LE 9-digit no dash
    sess.execute(
        """UPDATE detached_award_procurement AS dap
            SET legal_entity_county_code = zc.county_number,
                legal_entity_county_name = CASE WHEN dap.legal_entity_county_name IS NOT NULL 
                                                THEN dap.legal_entity_county_name
                                                ELSE UPPER(zc.county_name) END
            FROM zip_county AS zc
            WHERE zc.combined_zip = dap.legal_entity_zip4
                AND dap.legal_entity_county_code IS NULL
                AND UPPER(dap.legal_entity_country_code) = 'USA'"""
    )
    sess.commit()

    logger.info("Finished FPDS legal entity 9-digit zips without dashes, starting FPDS legal entity 9-digit zips "
                "with dashes")

    # FPDS LE 9-digit dash
    sess.execute(
        """UPDATE detached_award_procurement AS dap
            SET legal_entity_county_code = zc.county_number,
                legal_entity_county_name = CASE WHEN dap.legal_entity_county_name IS NOT NULL 
                                                THEN dap.legal_entity_county_name
                                                ELSE UPPER(zc.county_name) END
            FROM zip_county AS zc
            WHERE zc.dashed_zip = dap.legal_entity_zip4
                AND dap.legal_entity_county_code IS NULL
                AND UPPER(dap.legal_entity_country_code) = 'USA'"""
    )
    sess.commit()

    logger.info("Finished FPDS legal entity 9-digit zips with dashes, starting FPDS legal entity 5-digit zips")

    # FPDS LE 5-digit
    sess.execute(
        """UPDATE detached_award_procurement AS dap
            SET legal_entity_county_code = sc.county_number,
                legal_entity_county_name = CASE WHEN dap.legal_entity_county_name IS NOT NULL 
                                                THEN dap.legal_entity_county_name
                                                ELSE UPPER(sc.county_name) END
            FROM single_county AS sc
            WHERE sc.zip5 = LEFT(dap.legal_entity_zip4, 5)
                AND dap.legal_entity_county_code IS NULL
                AND dap.legal_entity_zip4 ~ '^\d{5}(-?\d{4})?$'
                AND UPPER(dap.legal_entity_country_code) = 'USA'"""
    )
    sess.commit()

    logger.info("Finished FPDS legal entity 5-digit zips, starting FPDS PPOP 9-digit zips without dashes")

    # FPDS PPOP 9-digit no dash
    sess.execute(
        """UPDATE detached_award_procurement AS dap
            SET place_of_perform_county_co = zc.county_number,
                place_of_perform_county_na = CASE WHEN dap.place_of_perform_county_na IS NOT NULL 
                                                  THEN dap.place_of_perform_county_na
                                                  ELSE UPPER(zc.county_name) END
            FROM zip_county AS zc
            WHERE zc.combined_zip = dap.place_of_performance_zip4a
                AND dap.place_of_perform_county_co IS NULL
                AND UPPER(dap.place_of_perform_country_c) = 'USA'"""
    )
    sess.commit()

    logger.info("Finished FPDS PPOP 9-digit zips without dashes, starting FPDS PPOP 9-digit zips with dashes")

    # FPDS PPOP 9-digit dash
    sess.execute(
        """UPDATE detached_award_procurement AS dap
            SET place_of_perform_county_co = zc.county_number,
                place_of_perform_county_na = CASE WHEN dap.place_of_perform_county_na IS NOT NULL 
                                                  THEN dap.place_of_perform_county_na
                                                  ELSE UPPER(zc.county_name) END
            FROM zip_county AS zc
            WHERE zc.dashed_zip = dap.place_of_performance_zip4a
                AND dap.place_of_perform_county_co IS NULL
                AND UPPER(dap.place_of_perform_country_c) = 'USA'"""
    )
    sess.commit()

    logger.info("Finished FPDS PPOP 9-digit zips with dashes, starting FPDS PPOP 5-digit zips")

    # FPDS PPOP 5-digit
    sess.execute(
        """UPDATE detached_award_procurement AS dap
            SET place_of_perform_county_co = sc.county_number,
                place_of_perform_county_na = CASE WHEN dap.place_of_perform_county_na IS NOT NULL 
                                                  THEN dap.place_of_perform_county_na
                                                  ELSE UPPER(sc.county_name) END
            FROM single_county AS sc
            WHERE sc.zip5 = LEFT(dap.place_of_performance_zip4a, 5)
                AND dap.place_of_perform_county_co IS NULL
                AND dap.place_of_performance_zip4a ~ '^\d{5}(-?\d{4})?$'
                AND UPPER(dap.place_of_perform_country_c) = 'USA'"""
    )
    sess.commit()

    logger.info("Finished FPDS PPOP 5-digit zips, starting FABS legal entity 9-digit zips")

    # FABS LE 9-digit
    sess.execute(
        """UPDATE published_award_financial_assistance AS pafa
            SET legal_entity_county_code = zc.county_number,
                legal_entity_county_name = CASE WHEN pafa.legal_entity_county_name IS NOT NULL 
                                                  THEN pafa.legal_entity_county_name
                                                  ELSE zc.county_name END
            FROM zip_county AS zc
            WHERE zc.zip5 = pafa.legal_entity_zip5
                AND zc.zip_last4 = pafa.legal_entity_zip_last4
                AND pafa.legal_entity_county_code IS NULL
                AND UPPER(pafa.legal_entity_country_code) = 'USA'
                AND pafa.is_active = True"""
    )
    sess.commit()

    logger.info("Finished FABS legal entity 9-digit zips, starting FABS legal entity 5-digit zips")

    #FABS LE 5-digit
    sess.execute(
        """UPDATE published_award_financial_assistance AS pafa
            SET legal_entity_county_code = sc.county_number,
                legal_entity_county_name = CASE WHEN pafa.legal_entity_county_name IS NOT NULL 
                                                  THEN pafa.legal_entity_county_name
                                                  ELSE sc.county_name END
            FROM single_county AS sc
            WHERE sc.zip5 = pafa.legal_entity_zip5
                AND pafa.legal_entity_county_code IS NULL
                AND UPPER(pafa.legal_entity_country_code) = 'USA'
                AND pafa.is_active = True"""
    )
    sess.commit()

    logger.info("Finished FABS legal entity 5-digit zips, starting FABS PPOP 9-digit zips without dashes")

    # FABS PPOP 9-digit no dash
    sess.execute(
        """UPDATE published_award_financial_assistance AS pafa
            SET place_of_perform_county_co = zc.county_number,
                place_of_perform_county_na = CASE WHEN pafa.place_of_perform_county_na IS NOT NULL 
                                                  THEN pafa.place_of_perform_county_na
                                                  ELSE zc.county_name END
            FROM zip_county AS zc
            WHERE zc.combined_zip = pafa.place_of_performance_zip4a
                AND pafa.place_of_perform_county_co IS NULL
                AND UPPER(pafa.place_of_perform_country_c) = 'USA'
                AND pafa.is_active = True"""
    )
    sess.commit()

    logger.info("Finished FPDS PPOP 9-digit zips without dashes, starting FABS PPOP 9-digit zips with dashes")

    # FABS PPOP 9-digit dash
    sess.execute(
        """UPDATE published_award_financial_assistance AS pafa
            SET place_of_perform_county_co = zc.county_number,
                place_of_perform_county_na = CASE WHEN pafa.place_of_perform_county_na IS NOT NULL 
                                                  THEN pafa.place_of_perform_county_na
                                                  ELSE zc.county_name END
            FROM zip_county AS zc
            WHERE zc.dashed_zip = pafa.place_of_performance_zip4a
                AND pafa.place_of_perform_county_co IS NULL
                AND UPPER(pafa.place_of_perform_country_c) = 'USA'
                AND pafa.is_active = True"""
    )
    sess.commit()

    logger.info("Finished FPDS PPOP 9-digit zips with dashes, starting FABS PPOP 5-digit zips")

    # FABS PPOP 5-digit
    sess.execute(
        """UPDATE published_award_financial_assistance AS pafa
            SET place_of_perform_county_co = sc.county_number,
                place_of_perform_county_na = CASE WHEN pafa.place_of_perform_county_na IS NOT NULL 
                                                  THEN pafa.place_of_perform_county_na
                                                  ELSE sc.county_name END
            FROM single_county AS sc
            WHERE sc.zip5 = LEFT(pafa.place_of_performance_zip4a, 5)
                AND pafa.place_of_perform_county_co IS NULL
                AND pafa.place_of_performance_zip4a ~ '^\d{5}(-?\d{4})?$'
                AND UPPER(pafa.place_of_perform_country_c) = 'USA'
                AND pafa.is_active = True"""
    )
    sess.commit()

    logger.info("Finished FPDS PPOP 5-digit zips, starting delete of temporary views")

    # zip_county view deletion
    sess.execute("DROP MATERIALIZED VIEW IF EXISTS single_county")
    sess.execute("DROP MATERIALIZED VIEW IF EXISTS zip_county")
    sess.commit()

    logger.info("Finished delete of temporary views, county code/name fix script complete")


if __name__ == '__main__':
    with create_app().app_context():
        configure_logging()
        main()