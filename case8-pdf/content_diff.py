import requests

# 你的两个文档内容
doc_version_1 = """
朱重八的高祖名叫朱百六，曾祖朱四九，祖父朱初一，父亲则是朱五四。如此
一串数字般的名字，并非源于什么数学家族的奇思妙想，而是那个时代底层百
姓生存状态的真实写照。元朝时期，若平民无缘学堂、无份官职，甚至连拥有
一个“名”的权利都没有。取名，成了户籍官随意而为的数字游戏，或父母年龄
相加，或出生日期相拼，由此造就了一个个听似荒诞实则辛酸的名字。
朱重八出生在一个极其贫寒的家庭。他的家，是一间“冬凉夏暖”、四面漏风的
茅草屋。屋顶时常漏雨，墙壁长满苔藓，地面坑洼不平。他从小便替地主刘德
放牛。天未亮便起身，牵着骨瘦如柴的老牛走向山野，直到夕阳沉没，才拖着
疲惫的身躯回到破屋。年复一年，寒暑不息。
他也曾对读书产生过憧憬。每当村中私塾传来朗朗书声，他总会悄悄趴在窗外
听上一会儿。他在地上划字、在泥墙上模仿先生的板书。他渴望那未知的文字
能带他走出困境。可现实无情，他的父亲朱五四连饭都供不起，更遑论学费。
他没有李密牛角挂书的志向，也无杨素遇贵人赏识的运气，只能继续放牛，因
为他要活命。
十六岁时，他想要成家。他托吴老太做媒，寻一位能吃苦的姑娘为妻。他憧憬
有朝一日生下几个儿女，或叫朱三二，或叫朱四零，将来送去给刘小德放牛。
这就是他彼时对生活最美的想象：能吃饱，能成家，有个归处。
可他的愿望，终究抵不过历史的洪流。彼时元朝统治日益腐败，蒙古贵族对中
原百姓视如草芥。百姓不仅无名，更无尊严。朝廷徭役繁重，税收繁多，凡有
名目的日子皆可收钱：“过节钱”、“常例钱”、“公事钱”，甚至连什么事都不干
也得缴“撒花钱”。如此酷政，使得民不聊生。
到了1344 年，大地震、黄河泛滥、瘟疫流行，一切仿佛天怒人怨。百姓口耳
相传一则民谣：“石人一只眼，挑动黄河天下反。”像是预言，又像是控诉。朱
重八听着这些传说，心中却越来越沉。村里饿死的人越来越多，草屋里时常传
出婴孩的哭声与老人的哀叹。
有一次，他在山坡上放牛时，遇到一位老和尚。和尚对他低声说：“你命硬福重，
将来能兴天下，记住，忍得一时，方可藏锋。”朱重八一笑置之，未将此话放心
上。但那天起，他的梦中频繁浮现金戈铁马、烈焰焚城的景象。他梦见百姓簇
拥他前行，呼喊他的名字。他不明所以，只觉心中起波澜。
元末动荡不安，各地义军蜂起。朱重八所在的村庄也卷入战乱，地主逃亡，民
众四散。他终于放下牛鞭，拿起锄头，踏上了一条截然不同的路。他初入起义
军，不过是个无名小卒。他赤脚行军，衣衫褴褛，但眼神愈发坚定。
在战乱中，他结识了一群志同道合之人。他善于倾听百姓之苦，体恤士兵之疾。
一次攻城，他为救受伤的同袍，独自夜潜敌营，将其背回，赢得众人敬重。他
不通兵法，却极具胆识与韧性。他用农人的逻辑打仗——求稳、用心、不贪、
不屈。
"""

doc_version_2 = """
朱重八的高祖名叫朱百六，曾祖是朱四九，祖父朱初一，父亲则是朱五四。乍
一看，朱家似乎和数学有不解之缘，从百六到五四，再到重八，像是一道代代
相传的等差数列。但这并非他们热爱算术，而是元朝一个特殊的历史背景造就
了这一奇异的命名传统。在那个时候，若是平民不能读书识字、不能做官，就
连名字也成了一种奢侈。他们只能依靠出生日期、父母年龄等粗略的数字信息
进行命名。于是，朱家一代代便有了这些看似随意、却又别具一格的名字。
朱重八的童年极其贫寒。他的家，是一间冬凉夏暖、四面通风、采光良好的破
茅草屋。所谓"良好"，不过是调侃罢了——寒风从屋缝中钻入，夏日烈阳透顶
直射。可这间茅屋，是朱家赖以生存的庇护所，是他人生最初的舞台。他的主
要工作是为地主刘德家放牛。天未亮，他便牵着瘦弱的老黄牛踏上山坡，日落
时分再一步步赶回来。一年三百六十五天，无论寒暑，从未间断。
朱重八小时候也曾对读书产生过幻想。他听村里教书的私塾先生吟诗作对、口
吐文墨，内心羡慕不已。他也曾试着用树枝在地上模仿写字。然而，朱五四实
在无力承担学费，更别提什么文房四宝了。他没有李密牛角挂书那样的勤学精
神，也无杨素那样的贵人相助。于是，梦想终究抵不过现实的残酷，他只能老
实地替刘德放了整整十二年的牛。因为，他要吃饭。
在这个过程中，朱重八渐渐习惯了沉默与坚韧。他不再幻想金榜题名，只希望
能踏踏实实活下去。到十六岁那年，他托村口吴老太做媒，想娶一个手脚勤快、
会干活的姑娘当媳妇。生下自己的孩子，或许叫朱三二，或者朱四零。他甚至
想好了，让这些孩子继续去地主刘小德家放牛，继续这样活下去。也许，这就
是他心中最大的幸福：有屋住，有饭吃，有儿女承欢膝下。
然而，他不知，这个卑微而温顺的愿望，注定无法如愿。在他所生活的中国，
元朝的统治已经腐烂透顶。蒙古贵族对汉人百姓毫无怜悯之心，把他们视作草
芥。曾有高官建议干脆把这些“占地方的家伙”全杀掉，再把土地用来放牧。
《元史》中记载的种种苛政让人不寒而栗。赋税繁重，徭役不断，凡是能想到
的名目都被用来搜刮民脂民膏：
过节要交“过节钱”；干活要交“常例钱”；打官司要交“公事钱”；就连待在家什
么都不干，也要交“撒花钱”。
这样的统治，让百姓苦不堪言。那些年，村里的人越来越穷，越来越沉默。灾
荒频发，疫病横行，饿殍遍野。而更令人绝望的是，希望似乎也在慢慢消失。
1344 年，这一年，老天终于决定对元朝“动手”了。那年，黄河改道成灾，泛滥
成灾，成千上万的百姓流离失所。同时，一种可怕的瘟疫自南而北迅速蔓延，
无数家庭倾覆。这一年，也传出了那句民谣：“石人一只眼，挑动黄河天下反。”
这句话如同妖言惑众，却又精准预言了即将而来的大乱。它像是某种天命的暗
示，像是从天地之间传来的谶语。而在茅屋中放牛的朱重八，尚不知道自己将
成为这个预言的“应验者”。他依旧每日牵牛上山，回村时目睹的是一户户破落
人家的哭声，是一个个被压榨至极的人。
"""

import requests

def compare_document_versions(doc_version_1, doc_version_2, model_name="qwen2.5:1.5b", ollama_url='http://localhost:11434/api/generate'):
    # 构建请求的数据
    prompt = f"请比较以下两个文档版本的内容，并详细列出它们的变化。\n\n版本1:\n{doc_version_1}\n\n版本2:\n{doc_version_2}"
    data = {
        "prompt": prompt,
        "stream": False,
        "model": model_name
    }

    # 发送请求到本地Ollama服务
    response = requests.post(ollama_url, json=data)

    # 检查请求是否成功
    if response.status_code == 200:
        # 获取并返回响应中的内容
        return response.json().get('response', '没有获取到响应内容')
    else:
        return f"请求失败，状态码: {response.status_code}"

# 使用示例

changes = compare_document_versions(doc_version_1, doc_version_2)
print(changes)
