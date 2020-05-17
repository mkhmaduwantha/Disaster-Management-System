import React, { Component } from "react";
import { popup } from "leaflet";
import axios from "axios";
import { Form, Button } from "react-bootstrap";
import { FaWindowClose } from "react-icons/fa";

class Message extends Component {
  constructor(props) {
    super(props);
    this.state = {
      //change the user id
      my_location: this.props.location,
      user_id: 1,
      currentStep: 1,
      subject: "",
      message: "",
      selected: false,
      radius: 0,
      military: false,
      refCamp: false,
      dmc: false,
      other: false,
      all: false,
    };
  }

  handleChange = (event) => {
    const { name, value } = event.target;
    this.setState({
      [name]: value,
    });
  };
  getOptionValue = (value) => {
    if (value === "military") {
      this.setState({
        military: !this.state.military,
      });
    } else if (value === "refCamp") {
      this.setState({
        refCamp: !this.state.refCamp,
      });
    } else if (value === "dmc") {
      this.setState({
        dmc: !this.state.dmc,
      });
    } else if (value === "other") {
      this.setState({
        other: !this.state.other,
      });
    } else if (value === "all") {
      this.setState({
        all: !this.state.all,
      });
    }
  };

  handleSubmit = (event) => {
    event.preventDefault();
    // console.log(this.props.props.history.push("/"));
    let data = {
      my_location: this.props.location,
      user_id: this.state.user_id,
      subject: this.state.subject,
      message: this.state.message,
      radius: this.state.radius,
      user_type: {
        military: this.state.military,
        ref_camp: this.state.ref_camp,
        dmc: this.state.dmc,
        other: this.state.other,
        all_user: this.state.all_user,
      },
    };
    axios({
      method: "post",
      url: "http://localhost:5000/map/notify",
      data: data,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    })
      .then(function (response) {
        console.log(response);
        alert(`Your Message Sent Successfully`);
      })
      .catch(function (response) {
        console.log(response);
        alert(response);
      });
    // axios.get("http://lcoalhost:5000/map/Message").then((res) => {
    //   console.log(res.data);
    // });
    // this.props.history.push("/chat");
  };
  _next = () => {
    let currentStep = this.state.currentStep;
    currentStep = currentStep >= 2 ? 3 : currentStep + 1;
    this.setState({
      currentStep: currentStep,
    });
  };

  _prev = () => {
    let currentStep = this.state.currentStep;
    currentStep = currentStep <= 1 ? 1 : currentStep - 1;
    this.setState({
      currentStep: currentStep,
    });
  };

  /*
   * the functions for our button
   */
  previousButton() {
    let currentStep = this.state.currentStep;
    if (currentStep !== 1) {
      return (
        <button
          className="btn btn-secondary prev-button"
          type="button"
          onClick={this._prev}
        >
          Previous
        </button>
      );
    }
    return null;
  }

  nextButton() {
    let currentStep = this.state.currentStep;
    if (currentStep < 3) {
      return (
        <button
          className="btn btn-primary float-right"
          type="button"
          onClick={this._next}
        >
          Next
        </button>
      );
    }
    return null;
  }

  render() {
    return (
      <React.Fragment>
        <h1>Notify Nearby Users </h1>
        <p>Step {this.state.currentStep} </p>
        <Button
          variant="secondary"
          onClick={this.props.closePopup}
          style={{
            display: "flex",
            justifyContent: "center",
            alignContent: "center",
            alignItems: "center",
            top: "1rem",
            position: "absolute",
            right: "1rem",
            padding: "0px",
            contentAlign: "center",
          }}
        >
          <FaWindowClose style={{ height: "1.5rem", width: "1.5rem" }} />
        </Button>
        <form onSubmit={this.handleSubmit}>
          {/* 
          render the form steps and pass required props in
        */}
          <Step1
            currentStep={this.state.currentStep}
            handleChange={this.handleChange}
            subject={this.state.subject}
            message={this.state.message}
          />
          <Step2
            currentStep={this.state.currentStep}
            handleChange={this.handleChange}
            radius={this.state.radius}
          />
          <Step3
            currentStep={this.state.currentStep}
            handleChange={this.handleChange}
            military={this.state.military}
            dmc={this.state.dmc}
            ref_camp={this.state.ref_camp}
            other={this.state.other}
            all_user={this.state.all_user}
            getOptionValue={this.getOptionValue}
          />
          {this.previousButton()}
          {this.nextButton()}
        </form>
      </React.Fragment>
    );
  }
}

function Step1(props) {
  if (props.currentStep !== 1) {
    return null;
  }
  return (
    <div className="form-group">
      <label htmlFor="subject">Subject</label>
      <input
        className="form-control"
        id="subject"
        name="subject"
        type="text"
        placeholder="Enter Subject"
        value={props.subject}
        onChange={props.handleChange}
      />
      <label htmlFor="message">Message</label>
      <input
        className="form-control"
        id="message"
        name="message"
        type="text"
        placeholder="Enter Message"
        value={props.message}
        onChange={props.handleChange}
      />
    </div>
  );
}

function Step2(props) {
  if (props.currentStep !== 2) {
    return null;
  }
  return (
    <div className="form-group">
      <label htmlFor="radius">Input a Radius (e.g: 1000 KM)</label>
      <input
        className="form-control"
        id="radius"
        name="radius"
        type="number"
        placeholder="Enter radius"
        value={props.radius}
        onChange={props.handleChange}
      />
    </div>
  );
}

// function Step3(props) {
//   if (props.currentStep !== 3) {
//     return null;
//   }
//   return (
//     <React.Fragment>
//       <div className="form-group">
//         <p>Receiver-Type</p>
//         <div className="custom-control custom-checkbox">

//           <input
//             type="checkbox"
//             className="custom-control-input"
//             id="military"
//             name="military"
//             checked={props.military}
//             onChange={props.handleChange}
//           />
//           <label className="custom-control-label" htmlFor="military">
//             Military
//           </label>
//         </div>
//         <div className="custom-control custom-checkbox">
//           <input
//             type="checkbox"
//             className="custom-control-input"
//             id="dmc"
//             name="dmc"
//             checked={props.dmc}
//             onChange={props.handleChange}
//           />
//           <label className="custom-control-label" htmlFor="dmc">
//             Disaster Management Centers
//           </label>
//         </div>

//         <div className="custom-control custom-checkbox">
//           <input
//             type="checkbox"
//             className="custom-control-input"
//             id="ref_camp"
//             name="ref_camp"
//             checked={props.ref_camp}
//             onChange={props.handleChange}
//           />
//           <label className="custom-control-label" htmlFor="ref_camp">
//             Refugee Camp
//           </label>
//         </div>
//         <div className="custom-control custom-checkbox">
//           <input
//             type="checkbox"
//             className="custom-control-input"
//             id="other"
//             name="other"
//             checked={props.other}
//             onChange={props.handleChange}
//           />
//           <label className="custom-control-label" htmlFor="other">
//             Other
//           </label>
//         </div>

//         <div className="custom-control custom-checkbox">
//           <input
//             type="checkbox"
//             className="custom-control-input"
//             id="all_user"
//             name="all_user"
//             checked={props.all_user}
//             onChange={props.handleChange}
//           />
//           <label className="custom-control-label" htmlFor="all_user">
//             All
//           </label>
//         </div>
//       </div>
//       <button className="btn btn-success btn-block">Submit</button>
//     </React.Fragment>
//   );
// }

function Step3(props) {
  if (props.currentStep !== 3) {
    return null;
  }
  return (
    <React.Fragment>
      <div className="form-group">
        <p>Receiver-Type</p>
        <div className="custom-control custom-checkbox">
          <>
            <Form.Group
              onChange={(e) => props.getOptionValue(e.target.value)}
              controlId="formBasicCheckbox"
            >
              <Form.Check value="military" type="checkbox" label="Military" />
              <Form.Check value="dmc" type="checkbox" label="DMC" />
              <Form.Check
                value="refCamp"
                type="checkbox"
                label="Refugee Camp"
              />
              <Form.Check value="other" type="checkbox" label="Other" />
              <Form.Check value="all" type="checkbox" label="All" />
            </Form.Group>
          </>
        </div>
      </div>
      <button
        style={{ float: "right", width: "85%" }}
        className="btn btn-success btn-block"
      >
        Submit
      </button>
    </React.Fragment>
  );
}

export default Message;
