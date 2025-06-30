# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MyFrame2
###########################################################################

class MyFrame2 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        self.m_menubar2 = wx.MenuBar( 0 )
        self.m_menu5 = wx.Menu()
        self.m_menuItem20 = wx.MenuItem( self.m_menu5, wx.ID_ANY, _(u"Opan"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu5.Append( self.m_menuItem20 )

        self.m_menuItem21 = wx.MenuItem( self.m_menu5, wx.ID_ANY, _(u"Ecsit"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu5.Append( self.m_menuItem21 )

        self.m_menubar2.Append( self.m_menu5, _(u"Faial") )

        self.m_menu6 = wx.Menu()
        self.m_menuItem22 = wx.MenuItem( self.m_menu6, wx.ID_ANY, _(u"Abaut"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu6.Append( self.m_menuItem22 )

        self.m_menubar2.Append( self.m_menu6, _(u"Hielp") )

        self.SetMenuBar( self.m_menubar2 )

        bSizer6 = wx.BoxSizer( wx.VERTICAL )


        bSizer6.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer7.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button4 = wx.Button( self, wx.ID_ANY, _(u"MyButton"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add( self.m_button4, 0, wx.ALL, 5 )


        bSizer6.Add( bSizer7, 0, wx.EXPAND, 5 )


        self.SetSizer( bSizer6 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_MENU, self.OnExit, id = self.m_menuItem21.GetId() )
        self.m_button4.Bind( wx.EVT_BUTTON, self.ClozeZaUindou )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnExit( self, event ):
        event.Skip()

    def ClozeZaUindou( self, event ):
        event.Skip()


