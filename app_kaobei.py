from flask import *
from datetime import datetime
from dbKaobei import *
import datetime
TODAY = datetime.date.today()
INTHREEDAYS = datetime.timedelta(days = 3)
app = Flask(__name__)

def get_KaobeiID():
    kaobeiid = KaobeiID.query.all()
    return kaobeiid

def get_KaobeiData():
    kaobeidata = KaobeiData.query.all()
    return kaobeidata

@app.route('/')
@app.route('/index')
def index():

    kaobeiid = get_KaobeiID()
    KaobeiID_dic = {}
    KaobeiID_list = []

    for _id in kaobeiid:
        total_like    = 0
        total_comment = 0
        total_share   = 0
        totalrank     = 0
        datainfo = KaobeiID.query.filter_by(FansPageID=_id.FansPageID).first()
        for info in datainfo.pages:
            total_like    += info.PostLike*1
            total_comment += info.PostComment*1.5
            total_share   += info.PostShare*2
            rank = total_like + total_comment + total_share
            KaobeiID_dic['Rank']      = rank
        KaobeiID_dic['FansPageID']    = _id.FansPageID
        KaobeiID_dic['KaobeiName']    = _id.KaobeiName
        KaobeiID_dic['KaobeiPicture'] = _id.KaobeiPicture
        KaobeiID_list.append(KaobeiID_dic)
        KaobeiID_dic = {}
    rank_list = sorted(KaobeiID_list, key = lambda e:e.__getitem__('Rank'), reverse=True)

    kaobeidata = get_KaobeiData()
    KaobeiData_dic = {}
    KaobeiData_list = []

    for _data in kaobeidata:
        total_like    = 0
        total_comment = 0
        total_share   = 0
        total         = 0

        posttime = _data.PostTime.date()
        if (posttime + INTHREEDAYS) >= TODAY:
            total_like    = _data.PostLike*1
            total_comment = _data.PostComment*1.5
            total_share   = _data.PostShare*2
            total = total_like + total_comment + total_share
            KaobeiData_dic['Rank']     = total
            KaobeiData_dic['PageID']   = _data.PageID
            KaobeiData_dic['PostID']   = _data.PostID
            KaobeiData_dic['PostTime'] = posttime
            KaobeiData_list.append(KaobeiData_dic)
            KaobeiData_dic = {}
    #post_weight = KaobeiData_list.sort(key=lambda k: (k.get('Rank', 0)), reverse=True)
    post_weight = sorted(KaobeiData_list, key = lambda e:e.__getitem__('Rank'), reverse=True)
    top_five = post_weight[:5]
    return render_template('index.html', **locals())

@app.route('/<kid>/<int:page_num>')
def kaobeifans(kid, page_num):
    kaobedata_pages = KaobeiData.query.filter_by(PageID=kid).order_by(KaobeiData.PostTime.desc()).paginate(per_page=10, page=page_num, error_out=True)
    pageid_list  = []
    kaobedata_all = get_KaobeiData()
    for info in kaobedata_all:
        pageid = info.PageID
        pageid_list.append(pageid)
    if kid not in pageid_list:
        kid = None
    return render_template("kaobeifans.html", kid=kid, kaobedata_pages=kaobedata_pages)
@app.route('/graph')
def echart():
    kaobeiid = get_KaobeiID()
    rank_weight_dic  = {}
    rank_weight_list = []
    rank_unweight_dic  = {}
    rank_unweight_list = []

    for item in kaobeiid:
        rank_like       = 0
        rank_comment    = 0
        rank_share      = 0
        un_rank_like    = 0
        un_rank_comment = 0
        un_rank_share   = 0
        rank_weight     = 0
        rank_unweight   = 0
        datainfo = KaobeiID.query.filter_by(FansPageID=item.FansPageID).first()
        for info in datainfo.pages:
            rank_like    += info.PostLike*1
            rank_comment += info.PostComment*1.5
            rank_share   += info.PostShare*2
            un_rank_like    += info.PostLike
            un_rank_comment += info.PostComment
            un_rank_share   += info.PostShare
            rank_weight = rank_like + rank_comment + rank_share
            rank_unweight = un_rank_like + un_rank_comment + un_rank_share
            rank_weight_dic['Rank']   = rank_weight
            rank_unweight_dic['Rank'] = rank_unweight
        rank_weight_dic['KaobeiName']   = item.KaobeiName
        rank_unweight_dic['KaobeiName'] = item.KaobeiName
        rank_weight_list.append(rank_weight_dic)
        rank_unweight_list.append(rank_unweight_dic)
        rank_weight_dic   = {}
        rank_unweight_dic = {}
    rank_weight_list = sorted(rank_weight_list, key = lambda e:e.__getitem__('Rank'), reverse=True)
    rank_unweight_list = sorted(rank_unweight_list, key = lambda e:e.__getitem__('Rank'), reverse=True)
    return render_template("echart.html", **locals())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)