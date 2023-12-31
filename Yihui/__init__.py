# 在 main.py 或者 __init__.py 中创建主类 Yihui
import warnings
import pandas as pd
import numpy as np
from Yihui.yihui import Yihui

# 在主程序中使用 Yihui 类
if __name__ == "__main__":
    # ban FutureWarning
    warnings.filterwarnings('ignore')

    # generate data.csv
    with open("../Data/data.csv", "r") as f:
        data = pd.read_csv(f)
    data['customer_no'] = str(data['customer_no'])
    data['v101'] = np.random.choice(['A', 'B', 'C', 'D', 'E', 'F'], size=len(data))

    # loading Titanic dataset
    # data = sns.load_dataset('titanic')
    # data.head()

    # Create Yihui Class
    yihui_project = Yihui(data, 'dlq_flag')
    print(yihui_project.data.head())

    print("Categorical Variables:", yihui_project.get_categorical_variables())
    print("Numeric Variables:", yihui_project.get_numeric_variables())

    # 直接访问 Yihui 类的属性获取字符型和数值型变量的名字
    categorical_vars_list = yihui_project.get_categorical_variables()
    numeric_vars_list = yihui_project.get_numeric_variables()

    eda_result = yihui_project.eda_module.auto_eda_simple()
    print(eda_result)


    # ### eda 阶段
    #
    # # 使用ydata_profiling 自动生成eda报告
    # # 根据dataset数据量大小，生成报告的时间会不同。建议慎重操作。
    # yihui_project.eda_module.auto_eda_profiling()
    #
    # # 手动查看变量分布情况
    # yihui_project.eda_module.plot_num_col(numeric_vars_list,plt_type='hist',plt_size=(100,100),plt_num=100,x=10,y=10)
    # yihui_project.eda_module.plot_num_col(numeric_vars_list,plt_type='box',plt_size=(100,100),plt_num=100,x=10,y=10)
    # yihui_project.eda_module.plot_cate_var(categorical_vars_list,plt_size=(100,100),plt_num=100,x=10,y=10)
    #
    # # 数值型变量的违约率分析
    # yihui_project.eda_module.plot_default_num(numeric_vars_list,q=10,plt_size=(100,100),plt_num=100,x=10,y=10)
    #
    # # 类别型变量的违约率分析
    # yihui_project.eda_module.plot_default_cate(categorical_vars_list,plt_size=(10,10),plt_num=1,x=1,y=1)
    #

    ### data processing 阶段

    # 所有变量缺失值分布图
    # print(yihui_project.dp_module.plot_bar_missing_var())

    # 使用 '0','median','class','rf'
    yihui_project.data = yihui_project.dp_module.fillna_num_var(numeric_vars_list, fill_type='0')
    #
    # yihui_project.data = yihui_project.dp_module.fillna_cate_var(categorical_vars_list, fill_type='class', fill_str='missing')
    # yihui_project.data = yihui_project.dp_module.fillna_cate_var(categorical_vars_list, fill_type='mode')
    #
    # # 缺失值剔除
    # yihui_project.data = yihui_project.dp_module.delete_missing_var(threshold=0.2)
    # yihui_project.data = yihui_project.dp_module.delete_missing_obs(threshold=5)

    # 常变量/同值化处理
    yihui_project.data = yihui_project.dp_module.const_delete(threshold=0.5)
    # print(yihui_project.dp_module.const_delete(threshold=0.9).columns)
    print(yihui_project.get_numeric_variables())

    yihui_project.data = yihui_project.dp_module.target_missing_delete()
    # 再检查一下缺失值
    # yihui_project.dp_module.plot_bar_missing_var()

    # # cluster 阶段

    # yihui_project.cluster_module.cluster_AffinityPropagation(['v1','v2']) # 非常慢，慎重
    # yihui_project.cluster_module.cluster_Birch(['v1','v2'])
    # yihui_project.cluster_module.cluster_GaussianMixture(['v2','v3'])
    # yihui_project.cluster_module.cluster_KMeans(['v3','v4'])


    # # binning 阶段
    # yihui_project.binning_module.binning_cate(categorical_vars_list)

    # print(yihui_project.binning_module.bin_df)

    # yihui_project.binning_module.binning_num(yihui_project.get_numeric_variables(), max_bin=20, min_binpct=0, method='ChiMerge')
    # yihui_project.binning_module.binning_num(['v1', 'v2', 'v3', 'v4'], max_bin=20, min_binpct=0, method='ChiMerge')
    # yihui_project.binning_module.iv_num(['v1', 'v2', 'v3', 'v4'], max_bin=20, min_binpct=0)
    # print(yihui_project.binning_module.iv_df)
    # yihui_project.binning_module.plot_woe(plt_size=(50,50),plt_num=4,x=2,y=2)


    # # var select 阶段
    # xg_fea_imp,xg_fea_imp_rank, xg_select_col = yihui_project.var_select_module.select_xgboost(yihui_project.get_numeric_variables())
    # print(xg_fea_imp)
    # print(xg_fea_imp['imp'].sum())
    # print(xg_select_col)

    # rf_fea_imp,  rf_select_col = yihui_project.var_select_module.select_rf(yihui_project.get_numeric_variables())
    # print(rf_fea_imp)
    # print(rf_fea_imp['imp'].sum())
    # print(rf_select_col)

    # yihui_project.var_select_module.plot_corr(yihui_project.get_numeric_variables(),0.5,'gt')
    #
    # corr_map_df = yihui_project.var_select_module.corr_mapping(yihui_project.get_numeric_variables(), threshold=0.5)
    # print(corr_map_df)
    #
    # list_corr = yihui_project.var_select_module.forward_delete_corr(yihui_project.get_numeric_variables(),0.5)
    # print(list_corr)
    # yihui_project.var_select_module.plot_corr(list_corr)
    #
    twice = yihui_project.var_select_module.forward_delete_corr_ivfirst(['v1','v2','v3','v4'],threshold=0.5)
    print(twice)

    twice = yihui_project.var_select_module.forward_delete_corr_impfirst(['v1','v2','v3','v4'],type='xgboost',threshold=0.5)
    print(twice)