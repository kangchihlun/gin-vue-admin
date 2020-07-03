package model

import (
	"github.com/jinzhu/gorm"
	uuid "github.com/satori/go.uuid"
)

type SysUser struct {
	gorm.Model
	UUID        uuid.UUID    `json:"uuid" gorm:"comment:'用户UUID'"`
	Username    string       `json:"userName" gorm:"comment:'用户登录名'"`
	Password    string       `json:"-"  gorm:"comment:'用户登录密码'"`
	Email       string       `json:"email" gorm:"default:'QMPlusUser'"`
	HeaderImg   string       `json:"headerImg" gorm:"default:'http://qmplusimg.henrongyi.top/head.png';comment:'用户头像'"`
	Authority   SysAuthority `json:"authority" gorm:"ForeignKey:AuthorityId;AssociationForeignKey:AuthorityId;comment:'用户角色'"`
	AuthorityId string       `json:"authorityId" gorm:"default:888;comment:'用户角色ID'"`
}
