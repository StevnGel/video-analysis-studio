import { Card, Statistic, Row, Col, Button, Typography } from 'antd'
import { VideoCameraOutlined, DatabaseOutlined, PlayCircleOutlined, AlertOutlined, SettingOutlined } from '@ant-design/icons'
import './Home.css'

const { Title, Paragraph } = Typography

function Home() {
  return (
    <div className="home-container">
      <Title level={2}>视频分析工作台</Title>
      <Paragraph>
        欢迎使用视频分析工作台，这是一个功能强大的视频分析系统，支持视频源管理、模型管理、任务管理、事件处理和配置管理等核心功能。
      </Paragraph>
      
      <Row gutter={[16, 16]} style={{ margin: '24px 0' }}>
        <Col span={6}>
          <Card hoverable>
            <Statistic
              title="视频源"
              value={10}
              prefix={<VideoCameraOutlined />}
              suffix="个"
            />
            <div className="card-actions">
              <Button type="primary" size="small" style={{ marginTop: 16 }}>
                管理视频源
              </Button>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card hoverable>
            <Statistic
              title="模型"
              value={5}
              prefix={<DatabaseOutlined />}
              suffix="个"
            />
            <div className="card-actions">
              <Button type="primary" size="small" style={{ marginTop: 16 }}>
                管理模型
              </Button>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card hoverable>
            <Statistic
              title="任务"
              value={8}
              prefix={<PlayCircleOutlined />}
              suffix="个"
            />
            <div className="card-actions">
              <Button type="primary" size="small" style={{ marginTop: 16 }}>
                管理任务
              </Button>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card hoverable>
            <Statistic
              title="事件"
              value={128}
              prefix={<AlertOutlined />}
              suffix="个"
            />
            <div className="card-actions">
              <Button type="primary" size="small" style={{ marginTop: 16 }}>
                查看事件
              </Button>
            </div>
          </Card>
        </Col>
      </Row>
      
      <Card title="系统状态" style={{ marginTop: 24 }}>
        <Row gutter={[16, 16]}>
          <Col span={8}>
            <Statistic title="CPU 使用率" value={45} suffix="%" />
          </Col>
          <Col span={8}>
            <Statistic title="内存使用率" value={60} suffix="%" />
          </Col>
          <Col span={8}>
            <Statistic title="磁盘使用率" value={30} suffix="%" />
          </Col>
        </Row>
        <div className="system-actions" style={{ marginTop: 24 }}>
          <Button type="primary" icon={<SettingOutlined />}>
            系统配置
          </Button>
        </div>
      </Card>
    </div>
  )
}

export default Home
