/* 3DView.Measurements
 * 
 * @author awesometeam / awesometeamone@gmail.com
 *
 * License: LGPL v3
 *
 */

////////////////////////////////////////////////////////////////////////////////
//MeasurementAngle class
////////////////////////////////////////////////////////////////////////////////
import {CylinderGeometry, Mesh, SphereGeometry, Vector3, TorusGeometry} from 'three';
import {Measurement, MeasurementGizmo, MeasurementGizmoMaterial} from './Measurement.js';
// import {MeasurementGizmoDistance} from './Measurement.Distance';

class MeasurementAngle extends Measurement {

	constructor(container) {        
		
		super();
		this.container = container;
		this.createGizmo = function(container) {
			this.measurementGizmo = new MeasurementGizmoAngle( this, container );
			return this.measurementGizmo;
		};

		this.getValue = function() {
			return this.measurementGizmo.getValue();
		};

		this.getInfo = function() {
			//get control points in world coordinates
			var controlPoints = this.measurementGizmo.getControlPointsWorld();
			
			var info = [];
			for (var i=0; i<Math.min(3, controlPoints.length); ++i) {
				info.push({name: 'Point '+ (i+1).toString()
				, values:[controlPoints[i].x, controlPoints[i].y, controlPoints[i].z]});
			}
			return info;
		};

		this.getType = function() {
			return 'Angle';
		};
		
		this.getDescription = function() {
			var value = this.getValue();
			if (value == null) return "angle";
			
			return 'angle = ' + this.getValue().toFixed(2) + String.fromCharCode(176);
		}
	}

}

export {MeasurementAngle}


////////////////////////////////////////////////////////////////////////////////////////////////
//class MeasurementGizmoAngle
////////////////////////////////////////////////////////////////////////////////////////////////
	
class MeasurementGizmoAngle extends MeasurementGizmo {
	constructor(measurement, container) {
        super();
        this.container = container;
        this.measurement = measurement;
		this.curveIn = true;
        const scope = this;

	this.handleGizmos = {

		'CURVE': [
			new Mesh( new TorusGeometry ( 10, 0.5, 2, 24, 0), new MeasurementGizmoMaterial( { color: 0x000000, opacity: 0.1 } ) )//Math.PI*2
		],
		'START': [
			new Mesh( new SphereGeometry( 2 ), new MeasurementGizmoMaterial( { color: 0xff0000, opacity: 0.4 } ) )
		],
		'MIDDLE': [
			new Mesh( new SphereGeometry( 2 ), new MeasurementGizmoMaterial( { color: 0xff0000, opacity: 0.4 } ) )
		],
		'END': [
			new Mesh( new SphereGeometry( 2 ), new MeasurementGizmoMaterial( { color: 0xff0000, opacity: 0.4 } ) )
		],
		'STARTLINE': [
			new Mesh( new CylinderGeometry( 1, 1, 1, 4, 1, false ), new MeasurementGizmoMaterial( { color: 0xff0000, opacity: 0.4 } ) ),
			new Vector3( 0, 0.5, 0 ),
			new Vector3( Math.PI/2, 0, 0 )
		],
		'ENDLINE': [
			new Mesh( new CylinderGeometry( 1, 1, 1, 4, 1, false ), new MeasurementGizmoMaterial( { color: 0xff0000, opacity: 0.4 } ) ),
			new Vector3( 0, 0.5, 0 ),
			new Vector3( Math.PI/2, 0, 0 )
		]
	}

	this.pickerGizmos = {

		'CURVE': [
			new Mesh( new TorusGeometry( 10, 0.5, 2, 24, 0 ), new MeasurementGizmoMaterial( { color: 0xff0000, opacity: 0.4 } ) )//Math.PI*2
		],
		'TEXT': [
			new Mesh( new SphereGeometry( 4 ), new MeasurementGizmoMaterial({visible: false}) )
		]

	}


	this.addControlPoint = function(point, object, forceAdd, face, callbackAddedObject) {
		
		var object = (scope.controlPoints.length < 3) ? object : scope.controlPoints[1].object; //for 4th point use object of the 2nd point
		MeasurementGizmo.prototype.addControlPoint.call(this, point, object, forceAdd, face, callbackAddedObject);
		
		if (scope.controlPoints.length == 2) {
			//2nd point - add measurement to object
			if (object) {
				object.add(this.measurement);
				if (callbackAddedObject) callbackAddedObject(this.measurement);
			}
			
		} 
		
		this.show();
	}
	
	this.acceptPoints = function() {
		return this.controlPoints.length < 3;
	}
	
	this.mustDragGizmo = function() {
		if (this.controlPoints.length == 3)
			return this.pickerGizmos['TEXT'][0];
		return false;
	}
	
	this.mustSnapToPart = function() {
		return this.controlPoints.length < 3;
	}
	
	this.update = function ( camera ) {
	
		//update gizmos
		if (this.isVisible()) {
			this.show();
			this.updateGizmosFromControlPoints( camera );
		} else {
			this.hide();
		}
	}		

	this.onGizmoMoved = function(gizmo, offset) {
		switch (gizmo) {
			case "CURVE":
			case "TEXT":
				if (this.controlPoints.length == 4) {
					var controlPoints = this.getControlPointsWorld();
					var cb = new Vector3().subVectors( controlPoints[2], controlPoints[1] );
					var ab = new Vector3().subVectors( controlPoints[0], controlPoints[1] );
					var pN = new Vector3().copy(cb).cross(ab);
					if (pN.length() > 0.0001) {
						//angle is not 0
						this.offsetControlPoint(3, new Vector3().copy(offset).projectOnPlane(pN));
						
					}
				}
				break;
		}
	}
	

	this.getValue = function() {
		if (this.controlPoints.length < 3) return null;

		//get points in local coordinates
		var controlPoints = scope.getControlPointsWorld();
		var vector1 = new Vector3().copy(controlPoints[1]).sub(controlPoints[0]);
		var vector2 = new Vector3().copy(controlPoints[1]).sub(controlPoints[2]);
		if (vector1.length() == 0 || vector2.length() == 0)
			return 0;
			
		var angle = vector1.angleTo(vector2) * 180 / Math.PI;
		if (!this.curveIn) angle = 360 - angle;
		
		return angle;
	};

	this.init();
	}

	updateGizmosFromControlPoints(camera) {
		var scope = this;
		//getting width
		var width = scope.getWidth(scope.getCenterPointWorld(), camera);
	
		var distance, correction;
		//get control points in world coordinates
		var controlPoints = scope.getControlPointsWorld();
		
		
		switch (scope.controlPoints.length) {
		
			
			case 4:
				
				//curve handle and picker
				var handle = scope.handleGizmos['CURVE'][0];
				var picker = scope.pickerGizmos['CURVE'][0];
				handle.visible = false;

				var bc = new Vector3().subVectors( controlPoints[1], controlPoints[2] );
				var ab = new Vector3().subVectors( controlPoints[0], controlPoints[1] );
				var pN = new Vector3().copy(bc).cross(ab);
				if (pN.length() > 0.0001) {
					//angle is not 0
					var referencePoint = this.projectPointToPlane(controlPoints[3], controlPoints[1], pN);
					var br = new Vector3().subVectors( referencePoint, controlPoints[1] );
					var aN = new Vector3().copy(ab).cross(br);
					var cN = new Vector3().copy(bc).cross(br);
					scope.curveIn = (pN.dot(aN) >= 0 && pN.dot(cN) >= 0);
					
					var arcAngle = scope.curveIn ? Math.PI - ab.angleTo(bc) : Math.PI + ab.angleTo(bc)
					var gizmoAngle = Math.PI/2;

					// handle.geometry.updateArc(arcAngle, false);
					// picker.geometry.updateArc(arcAngle, false);
					handle.geometry.arc = arcAngle;
					picker.geometry.arc = arcAngle;

					var radius = referencePoint.distanceTo(controlPoints[1]);
					ab.setLength(radius);
					var startPoint = new Vector3().copy(controlPoints[1]).sub(ab);
					bc.setLength(radius);
					var endPoint = new Vector3().copy(controlPoints[1]).sub(bc);
					
					handle.position.copy(controlPoints[1]);
					picker.position.copy(controlPoints[1]);
					handle.up.copy(pN);
					picker.up.copy(pN);
					if (scope.curveIn) {
						handle.lookAt(startPoint);
						picker.lookAt(startPoint);
					} else {
						handle.lookAt(endPoint);
						picker.lookAt(endPoint);
						gizmoAngle += Math.PI;
					}
					
					handle.rotateOnAxis(new Vector3(1,0,0), Math.PI/2*3);
					picker.rotateOnAxis(new Vector3(1,0,0), Math.PI/2*3);
					handle.rotateOnAxis(new Vector3(0,0,1), gizmoAngle);
					picker.rotateOnAxis(new Vector3(0,0,1), gizmoAngle);
					handle.scale.set(radius / 10.5, radius / 10.5, width) ;
					picker.scale.set(radius / 10.5, radius / 10.5, width) ;
					handle.visible = true;
					
				}


				//text picker
				var object = scope.pickerGizmos['TEXT'][0];
				object.position.copy(controlPoints[3]);
				object.scale.set(width, width, width);

				//set text value
				var angle = scope.getValue();
				scope.setText(angle.toFixed(2)+ String.fromCharCode(176), controlPoints[3], camera);
				
			case 3:
				//end point
				var pointWidth = scope.getWidth(controlPoints[2], camera);
				var object = scope.handleGizmos['END'][0];
				object.position.copy(controlPoints[2]);
				object.scale.set(pointWidth, pointWidth, pointWidth);
				object.visible = true;
				
				//end line
				distance = controlPoints[1].distanceTo(controlPoints[2]);
				if (radius) distance = Math.max(distance, radius);
				if (distance > 2*width) {
					var object = scope.handleGizmos['ENDLINE'][0];
					correction = new Vector3().copy(controlPoints[2]).sub(controlPoints[1]).setLength(width);
					
					object.position.copy(controlPoints[1]).add(correction);
					object.lookAt(controlPoints[2]);
					object.scale.set(width, width, distance-2*width);
					object.visible = true;
				} else scope.handleGizmos['ENDLINE'][0].visible = false;
				
			case 2:
				//middle point
				var pointWidth = scope.getWidth(controlPoints[1], camera);
				var object = scope.handleGizmos['MIDDLE'][0];
				object.position.copy(controlPoints[1]);
				object.scale.set(pointWidth, pointWidth, pointWidth);
				object.visible = true;
				
				//start line
				distance = controlPoints[0].distanceTo(controlPoints[1]);
				if (radius) distance = Math.max(distance, radius);
				if (distance > 2*width) {
					var object = scope.handleGizmos['STARTLINE'][0];
					correction = new Vector3().copy(controlPoints[1]).sub(controlPoints[0]).setLength(width);
					
					object.position.copy(controlPoints[1]).sub(correction);
					object.lookAt(controlPoints[0]);
					object.scale.set(width, width, distance-2*width);
					object.visible = true;
				} else scope.handleGizmos['STARTLINE'][0].visible = false;
				
				
			case 1:
				//start point
				var pointWidth = scope.getWidth(controlPoints[0], camera);
				var object = scope.handleGizmos['START'][0];
				object.position.copy(controlPoints[0]);
				object.scale.set(pointWidth, pointWidth, pointWidth);
				object.visible = true;
		}	
	}
	
	projectPointToPlane(point, planeOrigin, planeNormal) {
	
		return new Vector3().copy(point).sub(planeOrigin).projectOnPlane(planeNormal).add(planeOrigin);
		
	}
}

export {MeasurementGizmoAngle}