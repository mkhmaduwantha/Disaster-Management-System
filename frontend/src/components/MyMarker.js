import React, { Component } from "react";
import { popup, Icon } from "leaflet";
import axios from "axios";
import { FaWindowClose, FaLessThanEqual } from "react-icons/fa";
import { GiFlood } from "react-icons/gi";
import {
  Container,
  Row,
  Col,
  Image,
  Card,
  ButtonGroup,
  Button,
  Form,
  Modal,
} from "react-bootstrap";
import "./styles/MyMap.css";

class MyMarker extends Component {
  constructor(props) {
    super(props);
    this.state = {
      //change the user id
      my_location: this.props.location,
      user_id: 1,
      currentStep: 1,
      //marker states
      mType: "permanant",
      dType: "vAccident",
      subject: "",
      description: "",
      image: "",
    };
  }

  handleChange = (event) => {
    const { name, value } = event.target;
    this.setState({
      [name]: value,
    });
    console.log(this.state.dType);
  };

  getOptionValue = (value) => {
    this.setState({
      dType: value,
    });
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
      mtype: "permanant",
      address: "default",
      color: "red",
      name: "default",
      radius: 0,
      description: this.state.description,
      user_type: {
        military: this.state.military,
        ref_camp: this.state.ref_camp,
        dmc: this.state.dmc,
        other: this.state.other,
        all_user: this.state.all_user,
      },
    };
    this.props.addMyMarker(data);
    // axios({
    //   method: "post",
    //   url: "http://localhost:5000/map/notify",
    //   data: data
    // })
    //   .then(function (response) {
    //     console.log(response);
    //     alert(`Your Message Sent Successfully`);
    //   })
    //   .catch(function (response) {
    //     console.log(response);
    //     alert(response);
    //   });
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
        <h1>Add a Location </h1>
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
        <Form onSubmit={this.handleSubmit}>
          {/* 
          render the form steps and pass required props in
        */}
          <Step1
            currentStep={this.state.currentStep}
            getOptionValue={this.getOptionValue}
            dType={this.state.dType}
          />
          <Step2
            currentStep={this.state.currentStep}
            handleChange={this.handleChange}
            subject={this.state.subject}
            description={this.state.description}
          />
          <Step3
            currentStep={this.state.currentStep}
            handleChange={this.handleChange}
            image={this.state.image}
          />
          {this.previousButton()}
          {this.nextButton()}
        </Form>
      </React.Fragment>
    );
  }
}

function Step2(props) {
  if (props.currentStep !== 2) {
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
      <label htmlFor="description">Description</label>
      <Form.Control
        as="textarea"
        rows="3"
        name="description"
        placeholder="Enter Description"
        value={props.description}
        onChange={props.handleChange}
        required
      />
      <Form.Control.Feedback type="invalid">
        Please provide a Subject.
      </Form.Control.Feedback>
    </div>
  );
}

function Step3(props) {
  if (props.currentStep !== 3) {
    return null;
  }
  return (
    <React.Fragment>
      <div className="form-group">
        <Modal.Dialog>
          <Modal.Header>
            <Modal.Title>Add a Image or Submit</Modal.Title>
          </Modal.Header>

          <Modal.Body>
            <p>Image goes here.</p>
          </Modal.Body>

          <Modal.Footer>
            <Button variant="secondary">Choose</Button>
            <Button variant="primary">Camera</Button>
          </Modal.Footer>
        </Modal.Dialog>
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
// function Step1(props) {
//   if (props.currentStep !== 1) {
//     return null;
//   }
//   return (
//     <div className="form-group-1">
//       <ButtonGroup aria-label="Basic example">
//         <Button
//           variant="secondary"
//           style={{ marginLeft: "auto" }}
//           onClick={props.next}
//         >
//           <Image
//             src={require("./img/android-map-marker.png")}
//             style={{ width: "12rem" }}
//           ></Image>
//           <br></br>
//           <h5>Disaster Location</h5>
//         </Button>
//         <Button variant="secondary">
//           <Image
//             src={require("./img/marker-circle-red.png")}
//             style={{ width: "12rem" }}
//           ></Image>
//           <br></br>
//           <h5>Disaster Area</h5>
//         </Button>

//         <Button variant="secondary">
//           <Image
//             src={require("./img/hospitals-icon.png")}
//             style={{ width: "12rem" }}
//           ></Image>
//           <br></br>
//           <h5>Service Center</h5>
//         </Button>
//       </ButtonGroup>
//     </div>
//   );
// }

function Step1(props) {
  if (props.currentStep !== 1) {
    return null;
  }
  return (
    <div className="form-group">
      <Form.Group controlId="exampleForm.SelectCustomSizeLg">
        <Form.Label>Select a Disaster Type</Form.Label>
        <Form.Control
          as="select"
          size="lg"
          custom
          onChange={(e) => props.getOptionValue(e.target.value)}
        >
          <option value={"vAccident"}>Vehicle Accident</option>
          <option value={"landSlide"}>Land Slide</option>
          <option value={"bombBlast"}>Bomb Blast</option>
          <option value={"flood"}>Floods</option>
          <option value={"other"}>Other</option>
        </Form.Control>
      </Form.Group>
    </div>
  );
}

export default MyMarker;
