/* 3DView.Measurements
 * 
 * @author awesometeam / awesometeamone@gmail.com
 *
 * License: LGPL v3
 *
 */

//import { Measurement, MeasurementGizmo } from "./Measurement";
import { MeasurementDistance, MeasurementGizmoDistance } from "./Measurement.Distance.js";
import { computeFaceNormal } from "../3DView.Measurements.js";
import { Matrix3, Raycaster , Vector3 } from 'three';

////////////////////////////////////////////////////////////////////////////////
//MeasurementThickness class
////////////////////////////////////////////////////////////////////////////////

class MeasurementThickness extends MeasurementDistance{
	constructor(container){
		super();
		this.container = container;
		this.createGizmo = function(container){
			this.measurementGizmo = new MeasurementGizmoThickness(this,container);
			return this. measurementGizmo;
		};

		this.getType = function	() {
			return 'Thickness';
		}

		this.getDescription = function () {
			var value = this.getValue();
			if(value == null) return "thickness";
			return 'thickness = ' + this.getValue().toFixed(2);
		}


	}
}

export {MeasurementThickness}

//THREE.MeasurementThickness.prototype = Object.create( THREE.MeasurementDistance.prototype );


////////////////////////////////////////////////////////////////////////////////////////////////
//class MeasurementGizmoThickness
////////////////////////////////////////////////////////////////////////////////////////////////
	
class MeasurementGizmoThickness extends MeasurementGizmoDistance{
		constructor(measurement,container){
			super();
			this.container = container;
			this.measurement = measurement;
			const scope = this;

			this.addControlPoint = function(point, object, forceAdd, face, callbackAddedObject) {

				MeasurementGizmoDistance.prototype.addControlPoint.call(this, point, object, forceAdd, face, callbackAddedObject);
				
				if (scope.controlPoints.length == 1 && forceAdd !== true) {
					//get local normal
					var normal;
					
					//recalculate normal (just in case)
					if (object.geometry) {
						new computeFaceNormal(object.geometry, face);
					}
					normal = face.normal.clone();
					
					//compute negated world normal
					var normalMatrix = new Matrix3().getNormalMatrix( object.matrixWorld );
					var normalWorld = normal.clone().applyMatrix3( normalMatrix ).normalize().negate();

					//get next intersection across the normal
					var controlPoints = scope.getControlPointsWorld();
					const ray = new Raycaster();
					ray.set( controlPoints[0], normalWorld);
					var intersections = ray.intersectObjects( [object], true );
					
					var newPoint = controlPoints[0];
					for (var i=0; i<intersections.length; ++i) {
						var intersection = intersections[i];
						if (intersection.object && intersection.object.geometry) 
							new computeFaceNormal(intersection.object.geometry, intersection.face);
						if (normal.dot(intersection.face.normal) <= 0) {
							newPoint = intersections[i].point;
							break;
						}
					}
					
					MeasurementGizmoDistance.prototype.addControlPoint.call(this, newPoint, object, forceAdd, face, callbackAddedObject);
				}
			}

			this.updateGizmosFromControlPoints = function(camera) {
				MeasurementGizmoDistance.prototype.updateGizmosFromControlPoints.call(this, camera);
				
				var scope = this;
				var topPoints,horisontal,horisontalCorrection,arrowCorrection;
				if (scope.controlPoints.length < 2)
					return;
					
				//getting width
				var width = scope.getWidth(scope.getCenterPointWorld(), camera);
				
				var controlPoints = scope.getControlPointsWorld();
				//get top points
				if (scope.controlPoints.length == 4) 
					topPoints = [controlPoints[3], controlPoints[2]];
				else if (scope.controlPoints.length == 2) 
					topPoints = [controlPoints[0], controlPoints[1]];
				
				horisontal = new Vector3().copy(topPoints[1]).sub(topPoints[0]);
				horisontalCorrection = new Vector3().copy(horisontal).setLength(width * 3.0);
				arrowCorrection = new Vector3().copy(horisontal).setLength(width * 2.0);
				
				if (horisontal.length()-6*width > 0) {
				
					//top line
					var object = scope.handleGizmos['TOPLINE'][0];
					object.position.copy(topPoints[0]).add(horisontalCorrection);
					object.lookAt(topPoints[1]);
					object.scale.set(width, width, horisontal.length()-6*width);
					object.visible = true;
							
					//arrows
					var object = scope.handleGizmos['STARTARROW'][0];
					object.position.copy(topPoints[0]).add(arrowCorrection);
					object.lookAt(topPoints[1]);
					object.scale.set(width, width, width);
					object.visible = true;

					var object = scope.handleGizmos['ENDARROW'][0];
					object.position.copy(topPoints[1]).sub(arrowCorrection);
					object.lookAt(topPoints[0]);
					object.scale.set(width, width, width);
					object.visible = true;
					
				} else {
					scope.handleGizmos['TOPLINE'][0].visible = false;
					scope.handleGizmos['STARTARROW'][0].visible = false;
					scope.handleGizmos['ENDARROW'][0].visible = false;
				}

				//top line picker
				var object = scope.pickerGizmos['TOPLINE'][0];
				object.position.copy(topPoints[0]).add(horisontalCorrection);
				object.lookAt(topPoints[1]);
				object.scale.set(width, width, Math.max(horisontal.length()-6*width, 0.00001));
				
			}
			this.init();
	}
}
export {MeasurementGizmoThickness}