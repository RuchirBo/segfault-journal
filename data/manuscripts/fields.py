
TITLE = 'title'
DISP_NAME = 'disp_name'
AUTHOR = 'author'
AUTHOR_EMAIL = 'author_email'
REFEREES = 'referees'

TEST_FLD_NM = TITLE
TEST_FLD_DISP_NM = 'Title'

TEST_FLD_DISP_AUTHOR = 'Person'
TEST_FLD_DISP_REFEREE = 'Referee'


FIELDS = {
    TITLE: {
        DISP_NAME: TEST_FLD_DISP_NM,
    },
    AUTHOR: {
        DISP_NAME: TEST_FLD_DISP_AUTHOR,
    },
    REFEREES: {
        DISP_NAME: TEST_FLD_DISP_REFEREE,
    },
}


def get_flds() -> dict:
    return FIELDS


def get_fld_names() -> list:
    return FIELDS.keys()


def get_disp_name(fld_nm: str) -> dict:
    fld = FIELDS.get(fld_nm, '')
    return fld[DISP_NAME]  # should we use get() here?


def main():
    print(f'{get_flds()=}')


if __name__ == '__main__':
    main()