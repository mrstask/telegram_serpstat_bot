import os
from dotenv import load_dotenv
import logging


log = logging.getLogger("my-logger")

env = load_dotenv()

serpstat_regions = ['g_ua', 'g_ru', 'g_bg', 'g_kz', 'g_us', 'g_uk', 'g_ca', 'g_au', 'g_de', 'g_fr', 'g_es', 'g_it', 'g_lt', 'g_lv', 'g_ee', 'g_by', 'g_za', 'g_nl', 'g_br', 'g_il', 'g_dk', 'g_tr', 'g_se', 'g_cz', 'g_at', 'g_be', 'g_hu', 'g_no', 'g_fi', 'g_gr', 'g_pl', 'g_ro', 'g_pt', 'g_ie', 'g_ch', 'g_my', 'g_sg', 'g_th', 'g_si', 'g_hk', 'g_nz', 'g_cl', 'g_in', 'g_sk', 'g_sa', 'g_ae', 'g_ge', 'g_ar', 'g_vn', 'g_id', 'g_mx', 'g_co', 'g_ph', 'g_jp', 'g_tw', 'g_az', 'g_kg', 'g_kr', 'g_pe', 'g_hr', 'g_rs', 'g_md', 'g_ve', 'g_ec', 'g_ba', 'g_pk', 'g_eg', 'g_dz', 'g_ma', 'g_bo', 'g_uy', 'g_tn', 'g_do', 'g_cr', 'g_gt', 'g_lk', 'g_is', 'g_mk', 'g_am', 'y_213', 'y_2', 'y_187', 'y_54', 'y_47', 'y_65', 'y_35', 'y_157', 'g_af', 'g_bd', 'g_uz', 'g_ng', 'g_bn', 'g_pa', 'g_sv', 'g_py', 'g_hn', 'g_ke', 'g_pr', 'g_tt', 'g_jo', 'g_mu', 'g_re', 'g_ni', 'g_jm', 'g_iq', 'g_ps', 'g_gh', 'g_mt', 'g_al', 'g_qa', 'g_cy', 'g_lb', 'g_np', 'g_zw', 'g_mg', 'g_lu', 'g_ci', 'g_cm', 'g_kw', 'g_om', 'g_sn', 'g_ao', 'g_me', 'g_gp', 'g_mq', 'g_ye', 'g_kh', 'g_bh', 'g_tz', 'g_mz', 'g_nc', 'g_ly', 'g_mn', 'g_et', 'g_zm', 'g_na', 'g_pf', 'g_gf', 'g_ht', 'g_gy', 'g_fj', 'g_bz', 'g_bw', 'g_bs', 'g_ga', 'g_cd', 'g_mv', 'g_yt', 'g_sr', 'g_cv', 'g_gu', 'g_lc', 'g_ag', 'g_bj', 'g_ad', 'g_rw', 'g_la', 'g_vc', 'g_bf', 'g_aw', 'g_tj', 'g_gd', 'g_dj', 'g_tg', 'g_cg', 'g_mw', 'g_mr', 'g_mc', 'g_gn', 'g_kn', 'g_ky', 'g_bt', 'g_sc', 'g_ml', 'g_fo', 'g_vi', 'g_gi', 'g_ne', 'g_gq', 'y_39', 'g_ai', 'g_io', 'g_vg', 'g_td', 'g_ck', 'g_dm', 'g_fm', 'g_gm', 'g_gg', 'g_je', 'g_ki', 'g_li', 'g_ms', 'g_nu', 'g_nf', 'g_pg', 'g_pn', 'g_sm', 'g_st', 'g_sl', 'g_sb', 'g_tk', 'g_as', 'g_bi', 'g_cf', 'g_im', 'g_ls', 'g_nr', 'g_ws', 'g_so', 'g_to', 'g_ug', 'g_vu', 'g_cc', 'g_gl', 'g_bb', 'g_tl', 'g_cn', 'g_gw', 'g_km', 'g_lr', 'g_mh', 'g_pw', 'g_sz', 'g_tv', 'g_tm', 'g_er', 'g_va', 'g_mo', 'g_cx', 'g_bm', 'g_sh', 'g_tc', 'g_fk', 'g_mp', 'g_pm', 'g_wf', 'g_mm', 'g_cw']
serpstat_popular_regions = ['g_ua', 'g_ru', 'g_bg', 'g_kz', 'g_us', 'g_uk', 'g_ca', 'g_au', 'g_de', 'g_fr', 'g_es', 'g_it', 'g_lt', 'g_lv', 'g_ee', 'g_by', 'y_213', 'y_2', 'y_187', 'y_54', 'y_47', 'y_65', 'y_35', 'y_157']

develop = True if os.getenv('DEVELOP') == 'true' else False


class PostgresConfig:
    POSTGRES_DB_PORT = os.getenv('POSTGRES_DB_PORT')
    POSTGRES_DB_NAME = os.getenv('POSTGRES_DB_NAME')
    POSTGRES_DB_LOGIN = os.getenv('POSTGRES_DB_LOGIN')
    POSTGRES_DB_PASSWORD = os.getenv('POSTGRES_DB_PASSWORD')
    POSTGRES_DB_ADDRESS = os.getenv('POSTGRES_DB_ADDRESS')

    @property
    def postgres_db_path(self):
        return f'postgres://{self.POSTGRES_DB_LOGIN}:{self.POSTGRES_DB_PASSWORD}@' \
               f'{self.POSTGRES_DB_ADDRESS}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}'


class TelegramConf:
    API_KEY = os.getenv('TELEGRAM_API_KEY')


class SerpstatConf:
    HOST = 'http://api.serpstat.com/v3'
    API_KEY = ''


class HerokuConf:
    APP_URL = os.getenv('HEROKU_APP_URL')



