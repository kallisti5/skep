import Task from './task';

class Service extends React.Component {
  updateStatus() {
    const { updated, updating } = this.props.service;

    if (updating) {
      return (
        <span
          title={'Update in progress'}
          className={'updating'}
          data-toggle={'tooltip'}>
        </span>
      );
    }

    return (
      <span
        title={`Updated ${moment(updated).fromNow()}`}
        data-toggle={'tooltip'}
        data-placement={'top'}
        className={'updated'}>
        &#10003;
      </span>
    );
  }

  renderPorts() {
    const { ports, id } = this.props.service;

    return ports.map(
      mapping => (
        <div
          key={`service-${id}-${mapping.published}-${mapping.target}`}
          className={'ports'}>
          <span
            data-toggle={'tooltip'}
            title={'Published Port'}
            className={'published port'}>
            {':'}
            {mapping.published}
          </span>
          <span className={'published arrow'}>
            &#8615;
          </span>
          <span
            data-toggle={'tooltip'}
            title={'Target Port'}
            className={'target port'}>
            {':'}
            {mapping.target}
          </span>
          <span className={'target arrow'}>
            &#8613;
          </span>
        </div>
      )
    );
  }

  render() {
    const { name, image } = this.props.service;

    return (
      <div className={'service'}>

        <h2>
          {this.updateStatus()}
          <span className={'title'}>{name}</span>
          <span className={'tag'}>
            {`[${image.id}:${image.tag}]`}
          </span>
          {this.renderPorts()}
        </h2>

        <div className={'tasks'}>
          {this.props.service.tasks.map(task => (
            <Task
              key={task.id}
              task={task}
              manifest={this.props.manifest}
            />
          ))}
        </div>
      </div>
    );
  }
}

export default Service;