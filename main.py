# -*- coding: utf-8 -*-
"""
Script for the assessing impact of new rules on WWTP
Written by Svajunas Plunge
s.plunge@aaa.am.lt
"""
import data_cleaning
import transforming_table
import wwtp_ca_link
import extract_monitoring_links
import load_monitoring_data
import load_modeling_data
import q_wq_input_table
import q_wq_input_table_scenario
import wwpt_rules_apply
import present_results
data_cleaning.clean_lt_letters() #very slow
data_cleaning.data_clean()
transforming_table.transform_table()
wwtp_ca_link.wwtp_catchid_link()
extract_monitoring_links.extract_m_links()
load_monitoring_data.mon_data_prep()
load_modeling_data.mod_data_prep()
q_wq_input_table.prep_assessment_table()
q_wq_input_table_scenario.prep_assessment_table()
wwpt_rules_apply.eval_for_new_rules("baseline_plius")
present_results.wwtp_conc(GE_class=3, parameter="BOD7", ceilings=8, step=1, max_v=10)
present_results.comparison_fig("baseline_plius")
present_results.river_changes("no_agro_no_wwtp_final")
present_results.flow_compare(["baseline_final", "baseline_final_q05"])
present_results.concentrations()
present_results.concentrations_reaches()






