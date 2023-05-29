import pandas as pnd


class entity:
    def __init__(self, name: str):
        self.name = name


def bulk_groupby(input_df: pnd.DataFrame, groupby_entity: str) -> pnd.DataFrame:
    df = input_df[input_df['QTE_TRANS'] > 0].copy()
    month_prod_sums_df = df.groupby(['MOIS', 'PRODUIT']).agg({'QTE_TRANS': 'sum'})
    month_prod_sums_df.reset_index(inplace=True)
    month_prod_sums_df.rename(columns={'QTE_TRANS': 'QTE_TRANS_SUM'}, inplace=True)
    whole_saler_df = df.groupby(['MOIS', 'PRODUIT', groupby_entity]).agg({'QTE_TRANS': 'sum'})
    whole_saler_df.reset_index(inplace=True)
    whole_saler_df = pnd.merge(whole_saler_df, month_prod_sums_df, how='left', on=['MOIS', 'PRODUIT'])
    whole_saler_df['REPARTITION'] = whole_saler_df['QTE_TRANS'] / whole_saler_df['QTE_TRANS_SUM']
    concat_sort_df: pnd.DataFrame = pnd.DataFrame()
    for name, g_df in whole_saler_df.groupby(['MOIS', 'PRODUIT']):
        sort_df = g_df.sort_values(['REPARTITION'], ascending=False).copy()
        sort_df['RANK'] = range(1, 1 + sort_df.shape[0])
        concat_sort_df = pnd.concat([concat_sort_df, sort_df])

    month_sums_df = df.groupby('MOIS').agg({'QTE_TRANS': 'sum'})
    month_sums_df.reset_index(inplace=True)
    month_sums_df.rename(columns={'QTE_TRANS': 'QTE_TRANS_SUM'}, inplace=True)
    monthl_whole_saler_sums_df = df.groupby(['MOIS', groupby_entity]).agg({'QTE_TRANS': 'sum'})
    monthl_whole_saler_sums_df.reset_index(inplace=True)
    monthl_whole_saler_sums_df['PRODUIT'] = 'ALL SKUs'
    monthl_whole_saler_sums_df = pnd.merge(monthl_whole_saler_sums_df, month_sums_df, how='left', on=['MOIS'])
    monthl_whole_saler_sums_df['REPARTITION'] = monthl_whole_saler_sums_df['QTE_TRANS'] / monthl_whole_saler_sums_df[
        'QTE_TRANS_SUM']
    for name, g_df in monthl_whole_saler_sums_df.groupby(['MOIS']):
        sort_df = g_df.sort_values(['REPARTITION'], ascending=False).copy()
        sort_df['RANK'] = range(1, 1 + sort_df.shape[0])
        concat_sort_df = pnd.concat([concat_sort_df, sort_df])

    ytd_prod_sums_df = df.groupby(['PRODUIT']).agg({'QTE_TRANS': 'sum'})
    ytd_prod_sums_df.reset_index(inplace=True)
    ytd_prod_sums_df.rename(columns={'QTE_TRANS': 'QTE_TRANS_SUM'}, inplace=True)
    ytd_whole_saler_df = df.groupby(['PRODUIT', groupby_entity]).agg({'QTE_TRANS': 'sum'})
    ytd_whole_saler_df.reset_index(inplace=True)
    ytd_whole_saler_df = pnd.merge(ytd_whole_saler_df, ytd_prod_sums_df, how='left', on=['PRODUIT'])
    ytd_whole_saler_df['REPARTITION'] = ytd_whole_saler_df['QTE_TRANS'] / ytd_whole_saler_df['QTE_TRANS_SUM']
    ytd_whole_saler_df['MOIS'] = 'YTD'
    for name, g_df in ytd_whole_saler_df.groupby(['PRODUIT']):
        sort_df = g_df.sort_values(['REPARTITION'], ascending=False).copy()
        sort_df['RANK'] = range(1, 1 + sort_df.shape[0])
        concat_sort_df = pnd.concat([concat_sort_df, sort_df])

    ytd_sums = df['QTE_TRANS'].sum()
    ytd_whole_saler_sums_df = df.groupby([groupby_entity]).agg({'QTE_TRANS': 'sum'})
    ytd_whole_saler_sums_df.reset_index(inplace=True)
    ytd_whole_saler_sums_df['PRODUIT'] = 'ALL SKUs'
    ytd_whole_saler_sums_df['REPARTITION'] = ytd_whole_saler_sums_df['QTE_TRANS'] / ytd_sums
    ytd_whole_saler_sums_df['QTE_TRANS_SUM'] = ytd_sums
    ytd_whole_saler_sums_df['MOIS'] = 'YTD'
    ytd_whole_saler_sums_df.sort_values(['REPARTITION'], inplace=True, ascending=False)
    ytd_whole_saler_sums_df['RANK'] = range(1, 1 + ytd_whole_saler_sums_df.shape[0])
    concat_sort_df = pnd.concat([concat_sort_df, ytd_whole_saler_sums_df])

    concat_sort_df = concat_sort_df[
        ['MOIS', groupby_entity, 'RANK', 'PRODUIT', 'QTE_TRANS', 'QTE_TRANS_SUM', 'REPARTITION']]
    # rep_df.sort_values(['MOIS'], inplace=True)
    return concat_sort_df


input_df = pnd.read_excel('AT PHARMA.xlsx')
nom_df = bulk_groupby(input_df, 'NOM')
group_df = bulk_groupby(input_df, 'GROUPE_CLIENT')

writer = pnd.ExcelWriter('Répartition des ventes AT PHARMA.xlsx')
nom_df.to_excel(writer, sheet_name='Clients individuels', index=False)
group_df.to_excel(writer, sheet_name='Groupement clients', index=False)
writer.close()
