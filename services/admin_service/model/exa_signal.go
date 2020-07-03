package model

import (
	"time"

	"github.com/jinzhu/gorm"
)

type ExaSignal struct {
	gorm.Model

	SignalId       uint   `sql:"index" json:"signalId" form:"signalId" gorm:"comment:'策略編號'"`
	GroupId        uint   `json:"groupId" form:"groupId" gorm:"comment:'群組編號'"`
	SymbolCode     string `json:"symbolCode" form:"symbolCode" gorm:"comment:'商品代號'"`
	ExchangeCode   string `json:"exchangeCode" form:"exchangeCode" gorm:"comment:'交易所代碼'"`
	SignalName     string `json:"signalName" form:"signalName" gorm:"comment:'策略名稱'"`
	SignalInfo     string `json:"signalInfo" form:"signalInfo" gorm:"comment:'策略說明'"`
	SignalParmInfo string `json:"signalParmInfo" form:"signalParmInfo" gorm:"comment:'策略參數說明'"`
	ExitParmInfo   string `json:"exitParmInfo" form:"exitParmInfo" gorm:"comment:'策略出場參數說明'"`
	SignalCPInfo   string `json:"signalCPInfo" form:"signalCPInfo" gorm:"comment:'出場類型'"`
	SignalRefProd  string `json:"signalRefProd" form:"signalRefProd" gorm:"comment:'參考商品'"`
	SignalStatus   uint   `json:"signalStatus" form:"signalStatus" gorm:"comment:'是否上架'"`
	OpenBetaDate   time.Time
	OnLineDate     time.Time
	OffLineDate    time.Time
	Slippage       float32 `json:"slippage" form:"slippage" gorm:"comment:'滑價'"`
	Commission     float32 `json:"commission" form:"commission" gorm:"comment:'傭金'"`
	SignalPeriod   uint    `json:"signalPeriod" form:"signalPeriod" gorm:"comment:'時間週期'"`
	SignalType     string  `json:"signalType" form:"signalType" gorm:"comment:'策略型別'"`
	SignalFollow   uint    `json:"signalFollow" form:"signalFollow" gorm:"comment:'跟單人數上限'"`
	SignalCost     uint    `json:"signalCost" form:"signalCost" gorm:"comment:'策略費用'"`
	SignalAllot    uint    `json:"signalAllot" form:"signalAllot" gorm:"comment:''"`
	SignalMargin   uint    `json:"signalMargin" form:"signalMargin" gorm:"comment:'所需本金'"`
	IsDayTrade     uint    `json:"isDayTrade" form:"isDayTrade" gorm:"comment:'是否當沖'"`
	Route          string  `json:"route" form:"route" gorm:"comment:'參考商品'"`
}