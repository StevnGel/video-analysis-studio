import { useState } from 'react'
import { Outlet, Link, useLocation } from 'react-router-dom'
import { Layout as AntLayout, Menu, Button, theme } from 'antd'
import './Layout.css'

const { Header, Sider, Content } = AntLayout

function Layout() {
  const [collapsed, setCollapsed] = useState(false)
  const location = useLocation()

  const { token: { colorBgContainer, borderRadiusLG } } = theme.useToken()

  const menuItems = [
    {
      key: 'home',
      label: <Link to="/">首页</Link>,
    },
    {
      key: 'video-sources',
      label: <Link to="/video-sources">视频源管理</Link>,
    },
    {
      key: 'models',
      label: <Link to="/models">模型管理</Link>,
    },
    {
      key: 'tasks',
      label: <Link to="/tasks">任务管理</Link>,
    },
    {
      key: 'events',
      label: <Link to="/events">事件管理</Link>,
    },
    {
      key: 'configs',
      label: <Link to="/configs">配置管理</Link>,
    },
  ]

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Header className="header">
        <div className="logo">视频分析工作台</div>
        <div className="header-actions">
          <Button type="primary">登录</Button>
        </div>
      </Header>
      <AntLayout>
        <Sider
          collapsible
          collapsed={collapsed}
          onCollapse={(value) => setCollapsed(value)}
          style={{ background: colorBgContainer }}
        >
          <Menu
            mode="inline"
            selectedKeys={[location.pathname.substring(1) || 'home']}
            style={{ height: '100%', borderRight: 0 }}
            items={menuItems}
          />
        </Sider>
        <AntLayout style={{ padding: '0 24px 24px' }}>
          <Content
            style={{
              padding: 24,
              margin: 0,
              minHeight: 280,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            <Outlet />
          </Content>
        </AntLayout>
      </AntLayout>
    </AntLayout>
  )
}

export default Layout
