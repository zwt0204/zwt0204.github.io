# ASQ特征


## 特征
+ ideaid,wordid,unitid,planid,userid,title,mt_id,word,word_type,match_type,feed_ad_flag
>name=AdCreativeID;class=S_direct;slot=1;depend=ideaid;arg=int64（创意id）                                     
 name=AdWordID;class=S_direct;slot=2;depend=wordid;arg=int（触发词对应的id号）                                            
 name=UserId;class=S_direct;slot=3;depend=userid;arg=int（userid）                                              
 name=PlanId;class=S_direct;slot=4;depend=planid;arg=int64（计划id）                                     
 name=UnitId;class=S_direct;slot=5;depend=unitid;arg=int64（单元id）                                                                                      
 name=Title;class=S_direct;slot=9;depend=title;arg=str（广告title）                                                
 name=TitleTerm;class=S_word_seg;slot=10;depend=title;arg=10,1（广告title，分词）                                        
 name=WordnerInTitle;class=S_wordner;slot=11;depend=title;arg=NoTitleNer（广告title，命名实体识别）                              
 name=WordnerTypeInTitle;class=S_wordner_type;slot=12;depend=title（广告title，命名实体识别词语词性）                                                                               
 name=MtID;class=S_multi_new;slot=13;depend=mt_id;arg=str,#,1,0,0（物料类型-原始类型、蹊径）                                     
 name=BidWord;class=S_direct;slot=14;depend=word;arg=strquery/词包名/兴趣                                              
 name=BidWordTerm;class=S_word_seg;slot=15;depend=word;arg=10,1（query/词包名/兴趣）                                                                                                                                     
 name=WordType;class=S_direct;slot=16;depend=word_type;arg=str（词包来源）                                        
 name=MatchType;class=S_direct;slot=17;depend=match_type;arg=str（广告匹配方式）                                      
 name=FeedAdFlag;class=S_direct;slot=18;depend=feed_ad_flag;arg=str（是FC还是NKSAD）

+ cmatch && pid,cn,ip,ua,refer
>name=Cmatch;class=S_direct;slot=19;depend=cmatch;arg=int（广告位）                                             
 name=Pid;class=S_pid;slot=20;depend=pid（人所在的省份）                                                              
 name=ChargeName;class=S_direct;slot=21;depend=cn;arg=str（计费名，计费名确定广告（点击和展现）流量归属和收入归属的唯一标识）                                                     
 .name=Ip24;class=S_ip;slot=-524;depend=ip;arg=24（ip地址）                                                     
 .name=UserAgent;class=S_direct;slot=-525;depend=ua;arg=str（agent）                                           
 name=Ua;class=S_direct;slot=25;depend=ns_user_agent;arg=str（fix user agent）                                          
name=Refer;class=S_refer_comm;slot=27;depend=refer;arg=1|uid,baiduid,from,pu|uid,baiduid,from,pu,word,rawq,rawqs,rn,pn,st（fix refer）


+ cookieid,cuid,passport,age_id,gender_id,query_profile,gs_wise_multi_preq
>name=Cookieid;class=S_direct;slot=28;depend=cookieid;arg=str（baiduid）                                         
name=Cuid;class=S_direct;slot=29;depend=cuid;arg=str（cuid）                                                 
name=Passport;class=S_direct;slot=30;depend=passport;arg=str                                         
name=UserGender;class=S_direct;slot=31;depend=age_id;arg=str（年龄）                                         
name=UserAge;class=S_direct;slot=32;depend=gender_id;arg=str（性别）
name=ErisedTag;class=S_multi;slot=34;depend=query_profile;arg=str, ,10,0（用户profile，long_term_query）                             
name=Pre1Query;class=S_mul_preq_wise;slot=35;depend=gs_wise_multi_preq;arg=1,1,0（用户gs_session前文wise端的多阶query）                     
name=Pre2Query;class=S_mul_preq_wise;slot=36;depend=gs_wise_multi_preq;arg=2,1,0

+ combine
>idea
>>name=AdCreativeID-BidWord;class=S_combine;slot=38
>name=AdCreativeID-FeedAdFlag;class=S_combine;slot=42
>name=AdCreativeID-Cmatch;class=S_combine;slot=43
>name=AdCreativeID-Pid;class=S_combine;slot=44
>name=AdCreativeID-Cookieid;class=S_combine;slot=49
>name=AdCreativeID-Cuid;class=S_combine;slot=50
>name=AdCreativeID-UserGender-UserAge;class=S_anycombine;slot=52
>name=AdCreativeID-ErisedTag;class=S_combine;slot=53
>name=AdWordID-Cuid;class=S_combine;slot=58
>
>wordid
>>name=AdWordID-Cuid;class=S_combine;slot=58
>
>title
>>name=WordnerInTitle-WordType;class=S_combine;slot=70
>>name=WordnerInTitle-MatchType;class=S_combine;slot=71
>>name=WordnerInTitle-Cmatch;class=S_combine;slot=72
>name=WordnerInTitle-Cuid;class=S_combine;slot=74                                                     
>name=WordnerInTitle-Passport;class=S_combine;slot=75                                                 
>name=WordnerInTitle-UserGender-UserAge;class=S_anycombine;slot=76                                    
>name=WordnerInTitle-ErisedTag;class=S_combine;slot=77                                                
>name=WordnerInTitle-Pre1Query;class=S_combine;slot=78                                                
>name=WordnerInTitle-Pre2Query;class=S_combine;slot=79                                                
>name=TitleMatchedTermNum;class=S_matched_term_num;slot=80;depend=title,query_profile
>name=TitleTermNum;class=S_term_num;slot=73;depend=title
>
>match_type
>>name=MatchType-AdWordID;class=S_combine;slot=81
>name=MatchType-UserId;class=S_combine;slot=82
>name=MatchType-WordType;class=S_combine;slot=85
>name=MatchType-Cmatch;class=S_combine;slot=86 
>name=MatchType-Ua;class=S_combine;slot=87                                                            
>name=MatchType-Cookieid;class=S_combine;slot=88                                                      
>name=MatchType-Cuid;class=S_combine;slot=89                                                          
>name=MatchType-UserGender-UserAge;class=S_anycombine;slot=90
>
>FeedAdFlag
>>name=FeedAdFlag-Cuid;class=S_combine;slot=94
>
>cmatch
>>name=Cmatch-ChargeName;class=S_combine;slot=95
>>name=Cmatch-Cookieid;class=S_combine;slot=97
>>name=Cmatch-Cuid;class=S_combine;slot=98
>name=Cmatch-UserId;class=S_combine;slot=101                                                          
>name=Cmatch-PlanId;class=S_combine;slot=102                                                          
>name=Cmatch-UnitId;class=S_combine;slot=103
>
>cuid
>>name=Cuid-ChargeName;class=S_combine;slot=108
>>name=Cuid-UserAgent;class=S_combine;slot=110                                                         
>name=Cuid-Refer;class=S_combine;slot=111                                                             
>name=Cuid-AdCreativeID-MatchType;class=S_anycombine;slot=112                                         
>name=Cuid-AdCreativeID-Cmatch;class=S_anycombine;slot=113
>name=Cuid-AdCreativeID-UserAgent;class=S_anycombine;slot=116
>name=Cuid-AdCreativeID-Refer;class=S_anycombine;slot=117
>
+ profile
>name=TotalProfile;class=S_direct;slot=201;depend=total_profile;arg=stral_profile
>name=IdeaidProfile;class=S_multi_new;slot=202;depend=ideaid_profile;arg=str,^B,10,0,1（用户浏览广告兴趣点）
>name=MtidProfile;class=S_multi_new;slot=203;depend=mtid_profile;arg=str,^B,10,0,1（用户浏览广告样式趣点）
>name=CmatchProfile;class=S_multi_new;slot=204;depend=cmatch_profile;arg=str,^B,10,0,1（用户浏览广告cmatch点）
>name=RankProfile;class=S_multi_new;slot=205;depend=rank_profile;arg=str,^B,10,0,1（用户浏览广告rank兴趣点）
>name=TitleProfile;class=S_multi_new;slot=207;depend=title_profile;arg=str,^B,10,0,1（用户浏览广告title兴趣点）                  
>name=WordProfile;class=S_multi_new;slot=208;depend=word_profile;arg=str,^B,10,0,1（用户浏览广告word兴趣分布）

+ profile combine
>name=AdCreativeID-IdeaidProfile;class=S_combine;slot=251
>name=MtID-MtidProfile;class=S_combine;slot=252
>name=Title-TitleProfile;class=S_combine;slot=254
>name=Cuid-TotalProfile;class=S_combine;slot=255
>name=BidWord-WordProfile;class=S_combine;slot=256

+ 依赖字段：gs_feed_session_seq（在feedas中填充，记录feed的前文广告展现、自然点击和广告点击信息，由于自然点击获取不了rank信息，只拼接了广告展现和点击信息）
>name=GSWiseAdPreShwclk;class=S_session_adshwclk_wise;slot=263;depend=gs_feed_session_seq,ideaid;arg=1
>name=GSWiseAsAdClkSeq;class=S_npre_asadptn_wise;slot=265;depend=gs_feed_session_seq;arg=40,0

+ 依赖字段：gs_feed_time_list（记录feed的前文点击时间信息，包含广告和自然点击时间，由于自然点击过多，做了截断，最多只取5个）
>name=GSWisePre1QTimediff;class=S_mul_timediff_wise;slot=269;depend=cur_time,gs_feed_time_list;arg=1,1
>name=GSWiseSessionIfShow;class=S_session_ifshowed_wise;slot=274;depend=gs_feed_session_seq,ideaid;arg=0
>name=GSWisePpShowClkNum;class=S_session_stat_wise;slot=275;depend=gs_feed_session_seq;arg=0
>name=NewAdClkAvgGap;class=S_timediff_new;slot=276;depend=new_cur_time,gs_feed_time_list;arg=1,10,0
>name=NewSeClkAvgGap;class=S_timediff_new;slot=278;depend=new_cur_time,gs_feed_time_list;arg=3,10,0   
>name=NewSeClkGapSeq;class=S_timediff_new;slot=279;depend=new_cur_time,gs_feed_time_list;arg=4,10,0   
>name=NewSeSeGapSeq;class=S_timediff_new;slot=280;depend=new_cur_time,gs_feed_time_list;arg=5,10,0 

+ 依赖字段：gs_wise_title_list（global session中前文检索时点击的wise端的title序列）
>name=TitleTermTlMatchCntAdAs;class=S_session_term;slot=281;depend=gs_feed_title_list,title;arg=1,1,20,0,1
>name=TitleTermTlMatchStatAdAs;class=S_session_term;slot=287;depend=gs_feed_title_list,title;arg=1,1,20,20,1

+ 历史点击特征
>name=VideoSubCategoryHis;class=S_multi_new;slot=293;depend=gs_feed_video_sub_cat_his;arg=str,^B,10,0,1（在feedas中填充，记录feed的前文点击的视频二级分类）
>name=HpbFeedResource_pos_his;class=S_multi_new;slot=295;depend=gs_feed_pos_hist;arg=str,^B,10,0,1（记录feed的前文点击的位置）

+ wap personalization
>name=WordnerInTitle-Cookieid;class=S_combine;slot=310

+ XPilot 2 user long status
>.name=LongTrade2Status;class=S_multi_new;slot=-340;depend=long_trade2_status;arg=str,^B,10,0,1（原生广告用户对广告二级分类长线状态，由feed-as填充，格式 trade2 how次数-点击次数）       
>name=LongTrade3Status;class=S_multi_new;slot=341;depend=long_trade3_status;arg=str,^B,10,0,1 （原生广告用户对广告二级分类长线状态，由feed-as填充，格式 trade3 how次数-点击次数）        
>name=LongBrandStatus;class=S_multi_new;slot=342;depend=long_brand_status;arg=str,^B,10,0,1 （原生广告用户对广告品牌长线状态，由feed-as填充，格式 brand show次数-点击次数）
>name=UserId-LongTrade3Status;class=S_combine;slot=352                                                
>name=Brand;class=S_direct;slot=353;depend=brand;arg=str                                              
>name=Brand-LongBrandStatus;class=S_combine;slot=354
+ query word match_miss
>.name=WordMatchedTermNum;class=S_matched_term_num;slot=-14;depend=word,title

+ refresh status & refresh count
>name=RefreshState;class=S_direct;slot=365;depend=refresh_state;arg=str （用户的刷新状态，一般为整数）                              
>name=RefreshCount;class=S_direct;slot=366;depend=refresh_count;arg=str用户当前的刷新次数，一般为整数                               
>name=Cmatch-RefreshState;class=S_combine;slot=367                                                    
>name=Cmatch-RefreshCount;class=S_combine;slot=368                                                                                                                                                      
>name=EntityID;class=S_direct;slot=803;depend=entity_id;arg=str（广告主的实体标识）
>name=Trade2;class=S_feed_trade;slot=2010;depend=trade2;arg=2,988912（广告二级类目）                                  
>name=MtIDs;class=S_multi_new;slot=805;depend=mt_id;arg=str,#,10,0,1                                  
>name=Cuid-TitleTerm-RefreshState;class=S_anycombine;slot=816                                         
>name=Cuid-Brand-RefreshState;class=S_anycombine;slot=818                                             
>name=Cuid-Trade2-RefreshState;class=S_anycombine;slot=820                                            
>name=Cuid-EntityID-RefreshState;class=S_anycombine;slot=822                                          
>name=Cuid-MtIDs-RefreshState;class=S_anycombine;slot=824

+ XPilot 1&as profile & external session
>name=CategoryProfile;class=S_multi_new;slot=435;depend=category_profile;arg=str,^B,5,0,1
>name=AdCreativeID-CategoryProfile;class=S_combine;slot=436
>name=SubCateProfile;class=S_multi_new;slot=442;depend=site_profile;arg=str,^B,5,0,1
>name=AdCreativeID-SubCateProfile;class=S_combine;slot=445
>name=HostidOutNum;class=S_external_hostid;slot=449;depend=ex_list;arg=5,20(域外title)

+ User Environment
>name=FeedWordBranch;class=S_direct;slot=460;depend=word_branch;arg=int（广告word所属分支）                               
>name=FeedWordBranch-MatchType;class=S_combine;slot=461                                               
>name=FeedWordBranch-MatchType-BidWord;class=S_anycombine;slot=462

+ feed_virtual_mt_ids
>name=Wnettype;class=S_direct;slot=700;depend=wnettype;arg=int（wnettype，wifig，2g...）                                        
>name=Wosid;class=S_direct;slot=701;depend=wosid;arg=int（设备系统类型）                                              
>name=FeedVirtualMtIds;class=S_direct;slot=702;depend=feed_virtual_mt_ids;arg=str （广告的具体展示形式，比如：大图视频，wifi下自动播放）                    
>name=Cmatch-MtID-Wnettype-FeedVirtualMtIds;class=S_anycombine;slot=703                               
>name=Cmatch-MtID-Wosid-Wnettype-FeedVirtualMtIds;class=S_anycombine;slot=704                         
>name=Wosid-Wnettype;class=S_anycombine;slot=705

+ screen related
>name=ScreenWidth;class=S_direct;slot=706;depend=screenwidth;arg=int （屏幕宽度）                                 
>name=ScreenHeight;class=S_direct;slot=707;depend=screenheight;arg=int（屏幕高度）                                
>name=ScreenWidth-ScreenHeight;class=S_combine;slot=708                                               
>name=MtID-ScreenWidth-ScreenHeight;class=S_anycombine;slot=709                                                                                                                                       
>name=Cmatch-MtID-Wosid-Wnettype;class=S_anycombine;slot=710                                          
>name=Wosid-ScreenWidth-ScreenHeight;class=S_anycombine;slot=711                                      
>name=Wnettype-ScreenWidth-ScreenHeight;class=S_anycombine;slot=712

+ al4
>name=FeedPrimaryCategory;class=S_multi_new;slot=836;depend=feed_primary_feed_primary_category;arg=str,^B,10,0,1（用户新一级类别点展数据）   
>name=FeedSecondaryCategory;class=S_multi_new;slot=837;depend=feed_secondary_category;arg=str,^B,10,0,1（用户新二级类别点展数据）
>name=FeedNewsStyleSuper;class=S_multi_new;slot=838;depend=feed_news_style_super;arg=str,^B,10,0,1（用户格调特征点展数据-高端生活方式、高端趣味）    
>name=FeedAttentionDislike;class=S_multi_new;slot=839;depend=feed_attention_dislike;arg=str,^B,10,0,1（用户不喜欢文章的attention） 
>name=FeedAttentionVideo;class=S_multi_new;slot=840;depend=feed_attention_video;arg=str,^B,10,0,1（用户attention视频）     
>name=FeedVideoCategory;class=S_multi_new;slot=841;depend=feed_video_category;arg=str,^B,10,0,1（用户视频点展数据）       
>name=FeedVideoSubCategory;class=S_multi_new;slot=842;depend=feed_video_sub_category;arg=str,^B,10,0,1（用户视频分类点展数据）
>name=FeedAttentionShortAttentions;class=S_multi_new;slot=844;depend=feed_attention_short_attentions;arg=str,^B,10,0,1（feed用户模型数据short_attention）
>name=FeedAttentionStatics;class=S_multi_new;slot=845;depend=feed_attention_statics;arg=str,^B,10,0,1feed用户模型数据attention_statics

+ realtime（实时特征，24小时）
>name=RealtimeTotalStatus;class=S_direct;slot=900;depend=realtime_total_status;arg=str（原生广告用户实时状态，-click）                
>name=RealtimeIdeaidStatus;class=S_multi_new;slot=901;depend=realtime_ideaid_status;arg=str,^B,10,0,1（原生广告用户对创意实时状态） 
>name=RealtimeMtidStatus;class=S_multi_new;slot=902;depend=realtime_mtid_status;arg=str,^B,10,0,1（原生广告用户对样式实时状态）     
>name=RealtimeCmatchStatus;class=S_multi_new;slot=903;depend=realtime_cmatch_status;arg=str,^B,10,0,1（原生广告用户对广告投放渠道实时状态） 
>name=RealtimeRankStatus;class=S_multi_new;slot=904;depend=realtime_rank_status;arg=str,^B,10,0,1（原生广告用户对广告投放位置实时状态）     
>name=RealtimeCmatchRankStatus;class=S_multi_new;slot=905;depend=realtime_cmatch_rank_status;arg=str,^B,10,0,1（原生广告用户对广告投放组合实时状态）
>name=RealtimeWordStatus;class=S_multi_new;slot=906;depend=realtime_word_status;arg=str,^B,10,0,1（原生广告用户对广告词创意实时状态）     
>name=RealtimeTrade1Status;class=S_multi_new;slot=907;depend=realtime_trade1_status;arg=str,^B,10,0,1（原生广告用户对广告一级分类实时状态） 
>name=RealtimeTrade2Status;class=S_multi_new;slot=908;depend=realtime_trade2_status;arg=str,^B,10,0,1（原生广告用户对广告二级分类实时状态） 
>name=RealtimeTrade3Status;class=S_multi_new;slot=909;depend=realtime_trade3_status;arg=str,^B,10,0,1（原生广告用户对广告三级分类实时状态） 
>name=RealtimeBrandStatus;class=S_multi_new;slot=910;depend=realtime_brand_status;arg=str,^B,10,0,1（原生广告用户对广告品牌实时状态）

+ combine
> name=Cuid-RealtimeTotalStatus;class=S_combine;slot=913                                               
>name=AdCreativeID-RealtimeIdeaidStatus;class=S_combine;slot=914                                      
>name=MtID-RealtimeMtidStatus;class=S_combine;slot=915                                                
>name=Cmatch-RealtimeCmatchStatus;class=S_combine;slot=916                                            
>name=BidWord-RealtimeWordStatus;class=S_combine;slot=917                                             
>name=Brand-RealtimeBrandStatus;class=S_combine;slot=918                                              
>name=Trade2-RealtimeTrade2Status;class=S_combine;slot=919   

+ yizhixing
>name=NSUserAgent;class=S_direct;slot=925;depend=ns_user_agent;arg=str                                
>name=NSRefer;class=S_refer_comm;slot=927;depend=ns_refer;arg=1|uid,baiduid,from,pu|uid,baiduid,from,pu,word,rawq,rawqs,rn,pn,st

+ user center info
> name=CsidInfo;class=S_agg_session_info;slot=1040;depend=agg_session_info;arg=SessionInfoMulti,str,csid,0,10,0,1（agg_session_info为kv格式，用户中心特征）
>name=ThreadTitleInfo;class=S_agg_session_info;slot=1041;depend=agg_session_info;arg=SessionInfoMulti,str,thread_title,0,10,0,1
>name=UnionTitleForumDir;class=S_agg_session_info;slot=1042;depend=agg_session_info;arg=SessionInfoMulti,str,union_title_forum_dir,0,10,0,1
>name=UnionTitleForumSecDir;class=S_agg_session_info;slot=1043;depend=agg_session_info;arg=SessionInfoMulti,str,union_title_forum_second_dir,0,10,0,1
>name=Trade2Info;class=S_agg_session_info;slot=1044;depend=agg_session_info;arg=SessionInfoMulti,str,trade2,0,10,0,1
>name=BrandInfo;class=S_agg_session_info;slot=1045;depend=agg_session_info;arg=SessionInfoMulti,str,brand,0,10,0,1
>name=TitleInfo;class=S_agg_session_info;slot=1046;depend=agg_session_info;arg=SessionInfoMulti,str,title,0,10,0,1
>name=UnitidInfo;class=S_agg_session_info;slot=1047;depend=agg_session_info;arg=SessionInfoMulti,str,unitid,0,10,0,1

+ new
> name=LongCsidInfo;class=S_agg_session_info;slot=1050;depend=agg_session_info;arg=AggInfoMulti,str,csid_info,0,5,0,1
>name=LongMtInfo;class=S_agg_session_info;slot=1051;depend=agg_session_info;arg=AggInfoMulti,str,mt_info,0,5,0,1
>name=LongWordInfo;class=S_agg_session_info;slot=1052;depend=agg_session_info;arg=AggInfoMulti,str,word_info,0,5,0,1
>name=LongTrade2Info;class=S_agg_session_info;slot=1053;depend=agg_session_info;arg=AggInfoMulti,str,trade2_info,0,5,0,1
>name=LongBrandInfo;class=S_agg_session_info;slot=1054;depend=agg_session_info;arg=AggInfoMulti,str,brand_info,0,5,0,1
>name=MtIDFix;class=S_multi_new;slot=1039;depend=mt_id;arg=str,#,1,0,1

+ combine
>name=Cmatch-MtIDFix-Wnettype-FeedVirtualMtIds;class=S_anycombine;slot=1055                           
>name=Cmatch-MtIDFix-Wosid-Wnettype-FeedVirtualMtIds;class=S_anycombine;slot=1056                     
>name=MtIDFix-ScreenWidth-ScreenHeight;class=S_anycombine;slot=1057                                   
>name=Cmatch-MtIDFix-Wosid-Wnettype;class=S_anycombine;slot=1058                                      
>name=MtIDFix-RealtimeMtidStatus;class=S_combine;slot=1059                                            
>                                                                                                     
>name=Trade2-LongTrade2Info;class=S_combine;slot=1060                                                 
>name=ErisedTag-UnionTitleForumDir;class=S_combine;slot=1061                                          
>name=Brand-UnionTitleForumDir;class=S_combine;slot=1062                                              
>name=Title-ThreadTitleInfo;class=S_combine;slot=1063                                                 
>name=ErisedTag-ThreadTitleInfo;class=S_combine;slot=1064                                             
>name=WordnerInTitle-ThreadTitleInfo;class=S_combine;slot=1065

+ scvrq add slot
>name=DtApplist;class=S_multi_new;slot=2005;depend=dt_applist;arg=str,comma,10,0,1（画像-安装软件列表）                    
>name=DtStage;class=S_direct;slot=2006;depend=dt_stage;arg=str （画像-人生阶段）                                       
>name=DtAsset;class=S_direct;slot=2007;depend=dt_asset;arg=str （画像-资产状况）                                       
>name=DtEduLevel;class=S_direct;slot=2008;depend=dt_educational_level;arg=str（画像-教育水平）

+ update
>name=TransForm;class=S_direct;slot=1007;depend=at_flag;arg=str （用以记录AT_MATCH广告标识，17:query原文，33:精确地域，49:高级精确，65:高级短语，81:宽泛）                                      
>name=TransForm-Cmatch;class=S_combine;slot=1013                                                      
>name=TransForm-UserGender-UserAge;class=S_anycombine;slot=1014                                       
>name=Transtype;class=S_direct;slot=1017;depend=trans_type;arg=int （转化类型 ，区分不同的产品，ocpc,ocpm等，下同）                                   
>name=MiningType;class=S_direct;slot=2009;depend=mining_type;arg=int（ocpc实验室广告召回类型）                                  
>name=Trade2-Cmatch;class=S_combine;slot=2011                                                         
>name=Trade2-MatchType;class=S_combine;slot=2012                                                      
>name=Trade2-Wosid;class=S_combine;slot=2014                                                          
>name=Trade2-Wnettype;class=S_combine;slot=2015                                                       
>name=Trade2-Pid;class=S_combine;slot=2016                                                            
>name=Trade2-UserGender-UserAge;class=S_anycombine;slot=2017                                          
>name=Trade2-Ua;class=S_combine;slot=2018                                                             
>name=Brand-Cuid;class=S_combine;slot=2019                                                            
>name=Brand-BidWord;class=S_combine;slot=2020                                                         
>name=Brand-FeedAdFlag;class=S_combine;slot=2021                                                      
>name=Brand-Cmatch;class=S_combine;slot=2022                                                          
>name=Brand-Pid;class=S_combine;slot=2023                                                             
>name=Brand-UserGender-UserAge;class=S_anycombine;slot=2025                                           
>name=Brand-Ua;class=S_combine;slot=2026                                                              
>name=Brand-DtStage;class=S_combine;slot=2027                                                         
>name=Brand-DtAsset;class=S_combine;slot=2028                                                         
>name=Brand-DtEduLevel;class=S_combine;slot=2029                                                      
>name=UserId-Cuid;class=S_combine;slot=2045                                                           
>name=UserId-FeedAdFlag;class=S_combine;slot=2047                                                     
>name=UserId-Pid;class=S_combine;slot=2049                                                            
>name=UserId-Cookieid;class=S_combine;slot=2050                                                       
>name=UserId-UserGender-UserAge;class=S_anycombine;slot=2051                                          
>name=UserId-Ua;class=S_combine;slot=2052     
>name=UserId-DtStage;class=S_combine;slot=2053                                                        >name=UserId-DtAsset;class=S_combine;slot=2054                                                        
>name=UserId-DtEduLevel;class=S_combine;slot=2055                                                     
>name=UnitId-Cuid;class=S_combine;slot=2056                                                           
>name=UnitId-BidWord;class=S_combine;slot=2057                                                        
>name=UnitId-FeedAdFlag;class=S_combine;slot=2058                                                     
>name=UnitId-Pid;class=S_combine;slot=2060                                                            
>name=UnitId-UserGender-UserAge;class=S_anycombine;slot=2062                                          
>name=UnitId-DtStage;class=S_combine;slot=2064                                                        
>name=UnitId-DtAsset;class=S_combine;slot=2065                                                        
>name=UnitId-DtEduLevel;class=S_combine;slot=2066                                                     
>name=Brand-FeedAttentionVideo;class=S_combine;slot=2084                                              
>name=Brand-FeedAttentionShortAttentions;class=S_combine;slot=2085                                    
>name=Trade2-ErisedTag;class=S_combine;slot=2088                                                      
>name=Transtype-Trade2;class=S_combine;slot=2098                                                      
>name=Transtype-BidWord;class=S_combine;slot=2099                                                     
>name=Transtype-FeedAdFlag;class=S_combine;slot=2100                                                  
>name=Transtype-Cmatch;class=S_combine;slot=2111                                                      
>name=Transtype-Cookieid;class=S_combine;slot=2113                                                    
>name=Transtype-UserGender-UserAge;class=S_anycombine;slot=2114                                       
>name=Transtype-Ua;class=S_combine;slot=2115                                                          
>name=Transtype-DtStage;class=S_combine;slot=2116                                                     
>name=Transtype-DtAsset;class=S_combine;slot=2117                                                     
>name=Transtype-DtEduLevel;class=S_combine;slot=2118                                                  
>name=Transtype-ErisedTag;class=S_combine;slot=2120                                                   
>name=TradeID;class=S_direct;slot=1535;depend=trade2;arg=str                                          
>name=Transtype-MtID;class=S_combine;slot=1538                   