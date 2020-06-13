import React, { Component } from "react";
import {
  Modal,
  Button,
  Form,
  FormControl,
  Row,
  Col,
  Spinner,
} from "react-bootstrap";
import { storage, firebasedb } from "../config/firebasedb";
import { MdDelete } from "react-icons/md";
import { v4 as uuidv4 } from "uuid";

export class EditSafeLocation extends Component {
  constructor(props) {
    super(props);

    this.state = {
      id: "",
      name: "",
      phoneNo: "",
      category: "",
      noOfRefugees: "",
      headerImage: null,
      headerImgUrl: "",
      images: [],
      imagesUrls: [],
      imagesNewUrls: [],
      progress: 0,
      isUploading: false,
      preview: [],
    };
  }

  componentDidMount() {
    console.log(this.props.currentSafeLocation.id);
    this.setState({
      id: this.props.currentSafeLocation.id,
      name: this.props.currentSafeLocation.name,
      phoneNo: this.props.currentSafeLocation.phoneNo,
      category: this.props.currentSafeLocation.category,
      noOfRefugees: this.props.currentSafeLocation.noOfRefugees,
      imagesUrls: this.props.currentSafeLocation.imagesUrls,
    });
  }

  handleChange = (e) => {
    for (let i = 0; i < e.target.files.length; i++) {
      const newImage = e.target.files[i];
      const path = URL.createObjectURL(e.target.files[i]);
      newImage["id"] = Math.random();
      // add an "id" property to each File object
      // setFiles((prevState) => [...prevState, newFile]);
      this.setState((prevState) => {
        return {
          ...prevState,
          images: [...prevState.images, newImage],
          preview: [...prevState.preview, path],
        };
      });
    }
  };

  updateData = () => {
    let data = {
      name: this.state.name,
      phoneNo: this.state.phoneNo,
      category: this.state.category,
      noOfRefugees: this.state.noOfRefugees,
      imagesUrls: this.state.imagesUrls,
    };

    firebasedb
      .ref("places")
      .child(this.props.currentSafeLocation.id)
      .update(data)
      .then((snapshot) => snapshot.val())
      .catch((error) => ({
        errorCode: error.code,
        errorMessage: error.message,
      }));
  };

  // handleUpload = (e) => {
  //   console.log(this.state.images.length);
  //   this.setState({ isUploading: true });
  //   e.preventDefault();
  //   const promises = [];
  //   let counter = 0;
  //   this.setState({ isUploading: true });
  //   const { images } = this.state;
  //   images.forEach((image) => {
  //     const uploadTask = storage.ref("images/" + image.name).put(image);
  //     promises.push(uploadTask);
  //     uploadTask.on(
  //       "state_changed",
  //       (snapshot) => {
  //         //progress function
  //         const progress =
  //           Math.round(snapshot.bytesTransferred / snapshot.totalBytes) * 100;
  //         this.setState({ progress });
  //       },
  //       (error) => {
  //         //error function
  //         console.log(error);
  //       },
  //       () => {
  //         //complete function
  //         storage
  //           .ref("images")
  //           .child(image.name)
  //           .getDownloadURL()
  //           .then((url) => {
  //             this.setState(
  //               (prevState) => {
  //                 return {
  //                   ...prevState,
  //                   imagesUrls: [...prevState.imagesUrls, url],
  //                 };
  //               },
  //               () => {
  //                 counter++;
  //                 console.log(counter, url);
  //                 if (
  //                   this.state.images.length == this.state.imagesUrls.length
  //                 ) {
  //                   this.updateData();
  //                   this.setState({ isUploading: false });
  //                   setTimeout(() => {
  //                     this.setState({
  //                       name: "",
  //                       phoneNo: "",
  //                       category: "",
  //                       noOfRefugees: "",
  //                       headerImage: null,
  //                       headerImgUrl: "",
  //                       images: [],
  //                       imagesUrls: [],
  //                       progress: 0,
  //                       isUploading: false,
  //                       preview: [],
  //                     });
  //                   }, 4000);
  //                   alert("Submitted Successfully!");
  //                 }
  //               }
  //             );
  //             this.setState({ isUploading: false });
  //           });
  //       }
  //     );
  //   });
  // };

  handleUploadMultipleImages = (e) => {
    // e.preventDefault();
    console.log(this.state.images.length);
    const promises = [];
    let counter = 0;
    const { images } = this.state;
    if (images.length) {
      images.forEach((image) => {
        let uuid = uuidv4();
        const uploadTask = storage
          .ref("images/" + image.name + uuid)
          .put(image);
        promises.push(uploadTask);
        uploadTask.on(
          "state_changed",
          (snapshot) => {
            //progress function
            // const progress =
            //   Math.round(snapshot.bytesTransferred / snapshot.totalBytes) * 100;
            // this.setState({ progress });
          },
          (error) => {
            //error function
            console.log(error);
          },
          () => {
            //complete function
            storage
              .ref("images")
              .child(image.name + uuid)
              .getDownloadURL()
              .then((url) => {
                this.setState(
                  (prevState) => {
                    return {
                      ...prevState,
                      imagesUrls: [...prevState.imagesUrls, url],
                      imagesNewUrls: [...prevState.imagesNewUrls, url],
                    };
                  },
                  () => {
                    counter++;
                    console.log(counter, url);
                    if (
                      this.state.images.length ==
                      this.state.imagesNewUrls.length
                    ) {
                      this.updateData();
                      alert("Updated Successfully!");
                      this.props.onHide();
                    }
                  }
                );
              });
          }
        );
      });
    } else {
      this.updateData();
      alert("Updated Successfully!");
      this.props.onHide();
    }
  };

  deleteSafeLocation = () => {
    firebasedb.ref("places").child(this.props.currentSafeLocation.id).remove();
    alert("Deleted Successfully!");
    this.props.onHide();
  };

  render() {
    return (
      <div>
        <Modal
          {...this.props}
          size="lg"
          aria-labelledby="contained-modal-title-vcenter"
          centered
        >
          <Modal.Header closeButton>
            <Modal.Title id="contained-modal-title-vcenter">
              Set a Safe Place
            </Modal.Title>
          </Modal.Header>

          {/* Modal Body  */}
          <Modal.Body>
            <h4>Fill Below Details</h4>
            {/* Form  */}
            <Form>
              <Form.Group as={Row} controlId="formHorizontalEmail">
                <Form.Label column sm={2}>
                  Place name
                </Form.Label>
                <Col sm={10}>
                  <Form.Control
                    type="text"
                    placeholder="Name here..."
                    value={this.state.name}
                    onChange={(e) => this.setState({ name: e.target.value })}
                  />
                </Col>
              </Form.Group>

              <Form.Group as={Row} controlId="formHorizontalPassword">
                <Form.Label column sm={2}>
                  Phone No.
                </Form.Label>
                <Col sm={10}>
                  <Form.Control
                    type="text"
                    placeholder="Phone Number..."
                    value={this.state.phoneNo}
                    onChange={(e) => this.setState({ phoneNo: e.target.value })}
                  />
                </Col>
              </Form.Group>
              <fieldset>
                <Form.Group as={Row}>
                  <Form.Label as="legend" column sm={2}>
                    Category
                  </Form.Label>
                  <Col sm={10}>
                    <Form.Control
                      as="select"
                      value={this.state.category}
                      onChange={(e) =>
                        this.setState({ category: e.target.value })
                      }
                    >
                      <option>Choose One</option>
                      <option>School</option>
                      <option>Military Camp</option>
                      <option>Temple</option>
                      <option>Other</option>
                    </Form.Control>
                  </Col>
                </Form.Group>
              </fieldset>
              <Form.Group as={Row} controlId="formHorizontalEmail">
                <Form.Label column sm={5}>
                  No. of refugees that can be retained
                </Form.Label>
                <Col sm={7}>
                  <Form.Control
                    type="text"
                    placeholder="Approximately..."
                    value={this.state.noOfRefugees}
                    onChange={(e) =>
                      this.setState({ noOfRefugees: e.target.value })
                    }
                  />
                </Col>
              </Form.Group>

              {/* Image  */}
              <Form.Group controlId="exampleForm.ControlFile">
                <Form.Label style={{ float: "left" }}>
                  <b>Photos</b>
                </Form.Label>
                <Form.Control
                  type="file"
                  onChange={this.handleChange}
                  multiple
                  label={"Choose Photos"}
                />
              </Form.Group>
              {/* Spinner  */}
              {this.state.isUploading && (
                <div>
                  <Button variant="primary" disabled>
                    <Spinner
                      as="span"
                      animation="grow"
                      size="sm"
                      role="status"
                      aria-hidden="true"
                    />
                    Submitting...
                  </Button>
                </div>
              )}
              <Row>
                <Form.Group as={Row} style={{ margin: 3 }}>
                  <Col sm={{ span: 10, offset: 2 }}>
                    <Button onClick={this.handleUploadMultipleImages}>
                      Update
                    </Button>
                  </Col>
                </Form.Group>
                <Form.Group as={Row} style={{ margin: 3 }}>
                  <Col sm={{ span: 10, offset: 2 }}>
                    <Button onClick={this.deleteSafeLocation} variant="danger">
                      Delete
                    </Button>
                  </Col>
                </Form.Group>
              </Row>
            </Form>
            <Row>
              {this.state.imagesUrls &&
                this.state.imagesUrls.map((url) => {
                  if (url != "") {
                    return (
                      <Col
                        xl={4}
                        xs={12}
                        style={{
                          overflow: "hidden",
                          // margin: 10,
                          // marginHorizontal: 25,
                        }}
                      >
                        <div>
                          <img
                            src={url}
                            alt="HJ"
                            width="40%"
                            style={{ margin: 2 }}
                          />
                          <Button
                            variant="light"
                            onClick={() => {
                              var filteredItems = this.state.imagesUrls.filter(
                                (item) => item != url
                              );
                              this.setState({ imagesUrls: filteredItems });
                            }}
                            style={{
                              height: 40,
                              // marginLeft: 20,
                            }}
                          >
                            <MdDelete style={{ color: "red" }} /> Remove
                          </Button>
                        </div>
                      </Col>
                    );
                  }
                })}
            </Row>
          </Modal.Body>

          <Modal.Footer>
            <Button onClick={this.props.onHide}>Close</Button>
          </Modal.Footer>
        </Modal>
      </div>
    );
  }
}

export default EditSafeLocation;
